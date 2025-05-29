import re
import os
from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
import replicate

import json

from prompts import BOOK_TEXT_PROMPT, get_visual_description_function, get_lighting_and_atmosphere_function, get_character_reference_function
from deep_lake_utils import SaveToDeepLake

import requests

import streamlit as st

load_dotenv('keys.env')


class BuildBook:  # The do-it-all class that builds the book (and creates streamlit elements!)
    book_text_prompt = BOOK_TEXT_PROMPT

    def __init__(self, model_name, input_text, style):
        self.chat = ChatOpenAI(model=model_name)
        self.input_text = input_text
        self.style = style
        self.seed = 42  # Fixed seed for all images

        self.progress = st.progress(0)
        self.progress_steps = 0
        self.total_progress_steps = 30

        self.progress_steps += 2
        self.progress.progress(self.progress_steps / self.total_progress_steps, "Generating book text...")
        self.book_text = self.get_pages()

        self.progress_steps += 2
        self.progress.progress(self.progress_steps / self.total_progress_steps, "Generating SD prompts...")

        self.pages_list = self.get_list_from_text(self.book_text)

        self.sd_prompts_list = self.get_prompts()

        self.source_files = self.download_images()
        
        # Try to save to Deep Lake if available, but continue if it fails
        try:
            if os.getenv('DATASET_PATH') and os.getenv('DATASET_PATH') != 'path here':
                self.progress_steps += 1
                self.progress.progress(self.progress_steps/self.total_progress_steps, "Saving to Deep Lake...")
                self.ds = SaveToDeepLake(self, dataset_path=os.getenv('DATASET_PATH'))
                self.ds.fill_dataset()
        except Exception as e:
            print(f"Deep Lake storage skipped: {e}")
        
        self.list_of_tuples = self.create_list_of_tuples()
        self.progress.progress(1.0, "Done! Wait one moment while your book is processed...")

    def get_pages(self):
        pages = self.chat([HumanMessage(content=f'{self.book_text_prompt} Topic: {self.input_text}')]).content
        return pages

    def get_prompts(self):
        base_atmosphere = self.chat([HumanMessage(
            content=f'Generate a visual description of the overall lightning/atmosphere of this book using the function.'
                    f'{self.book_text}')], functions=get_lighting_and_atmosphere_function)
        base_dict = func_json_to_dict(base_atmosphere)

        # Get consistent character reference
        character_ref = self.chat(
            [HumanMessage(content=f'Extract consistent character descriptions from: {self.book_text}')],
            functions=get_character_reference_function
        )

        character_ref = self.chat(                                                                                                                                             
            [HumanMessage(content=(                                                                                                                                            
                f'Extract and define consistent visual attributes for all characters from: {self.book_text}. '                                                                 
                'If the book text does not specify an attribute, invent one that fits the story. '                                                                            
                'Include every main character and specify all required attributes (hair, eyes, clothing, height).'                                                            
                ))],                                                                                                                                                               
                functions=get_character_reference_function                                                                                                                         
            )                                                                                                                                                                      
     
        character_descriptions = func_json_to_dict(character_ref)['character_descriptions']

        summary = self.chat(
            [HumanMessage(content=f'Generate a concise summary of the setting and visual details of the book')]).content

        base_dict['summary_of_book_visuals'] = summary
        base_dict['character_descriptions'] = character_descriptions
        
        self.debug_info = []  # Store page text and prompts for debugging

        def generate_prompt(page, base_dict):
            prompt = self.chat(
                [HumanMessage(content=(
                    f'Visual description for: "{page}"\n\n'
                    f'STRICT RULES:\n'
                    f'1. USE THESE EXACT CHARACTER ATTRIBUTES: {base_dict["character_descriptions"]}\n'
                    f'2. NEVER CHANGE: Hair color/length, eye color, clothing patterns/colors\n'
                    f'3. PRESERVE HEIGHTS: Characters must maintain consistent relative heights\n'
                    f'4. INCLUDE ALL ATTRIBUTES: Explicitly mention hair, eyes, clothing in every description\n'
                    f'Focus on characters and actions. '
                    f'Atmosphere: {base_dict}. Style: {self.style}'
                ))],
                functions=get_visual_description_function)
            enhanced_visual = func_json_to_dict(prompt)['enhanced_visual']
            
            # Extract character names from descriptions to add weighting
            character_names = []
            char_desc = base_dict["character_descriptions"]
            # Simple extraction - looks for capitalized words that might be names
            import re
            potential_names = re.findall(r'\b[A-Z][a-z]+\b', char_desc)
            # Filter out common non-name capitalized words
            common_words = ["The", "A", "An", "In", "On", "At", "With"]
            character_names = [name for name in potential_names if name not in common_words]
            
            # Add character weighting if names were found
            if character_names:
                character_weights = " ".join([
                    f"({name} with {char_desc.split(name)[1].split('.')[0] if name in char_desc else ''}:1.5)" 
                    for name in character_names
                ])
                final_prompt = f"{character_weights} {enhanced_visual}, in the style of {self.style}"
            else:
                final_prompt = f"{enhanced_visual}, in the style of {self.style}"
            
            # Store debug info
            self.debug_info.append({
                'page_text': page,
                'enhanced_visual': enhanced_visual,
                'final_prompt': final_prompt
            })
            
            return enhanced_visual  # Return just the enhanced text

        with ThreadPoolExecutor(max_workers=10) as executor:
            prompts = list(executor.map(generate_prompt, self.pages_list, [base_dict] * len(self.pages_list)))
        
        # Store base_dict for consistency checks
        self.base_dict = base_dict
        
        # Check character consistency
        self.check_character_consistency()
        
        # Print debug info to console
        print("\n" + "="*80)
        print("DEBUG: PAGE TEXT TO SD PROMPT MAPPING")
        for i, item in enumerate(self.debug_info):
            print(f"\nPage {i+1} Text:\n{item['page_text']}")
            print(f"\nEnhanced Visual:\n{item['enhanced_visual']}")
            print(f"\nFinal SD Prompt:\n{item['final_prompt']}")
        print("="*80)
        
        # Add style suffix to each prompt
        return [f"{p}, in the style of {self.style}" for p in prompts]
    
    def check_character_consistency(self):
        """Verify all prompts contain required attributes"""
        required_attributes = ["hair", "eyes", "clothing"]
        for i, item in enumerate(self.debug_info):
            prompt = item['final_prompt']
            missing = [attr for attr in required_attributes if attr not in prompt.lower()]
            if missing:
                print(f"WARNING: Page {i+1} missing {', '.join(missing)} attributes")
                # Auto-correct missing attributes
                corrected = prompt + f". {self.base_dict['character_descriptions']}"
                self.debug_info[i]['final_prompt'] = corrected
                print(f"Auto-corrected prompt: {corrected}")

    def get_list_from_text(self, text):
        new_list = re.split(r'Page \d+:', text)
        new_list.pop(0)
        return new_list

    def create_images(self):
        if len(self.pages_list) != len(self.sd_prompts_list):
            raise 'Pages and Prompts do not match'

        def generate_image(i, prompt):
            print(f'{prompt} is the prompt for page {i + 1}')

            # output = replicate.run(
            #     "stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf",
            #     input={"prompt": 'art,' + prompt,
            #            "seed": self.seed,  # Fixed seed for consistency
            #            "negative_prompt": "photorealistic, photograph, bad anatomy, blurry, gross,"
            #                               "weird eyes, creepy, text, words, letters, realistic"
            #            },
            # )

            output = replicate.run(
                "google/imagen-4",
                input={
                    "prompt": 'art,' + prompt,
                    "aspect_ratio": "16:9",
                    "safety_filter_level": "block_low_and_above"
                }
            )

            return output[0]

        with ThreadPoolExecutor(max_workers=10) as executor:
            image_urls = list(executor.map(generate_image, range(len(self.sd_prompts_list)), self.sd_prompts_list))

        return image_urls

    def download_images(self):
        image_urls = self.create_images()
        source_files = []
        for i, url in enumerate(image_urls):
            r = requests.get(url, stream=True)
            file_path = f'images/{i + 1}.png'
            with open(file_path, 'wb') as file:
                source_files.append(file_path)
                for chunk in r.iter_content():
                    file.write(chunk)
                self.progress_steps += 1
                self.progress.progress(self.progress_steps / self.total_progress_steps, f"Downloading image {i + 1}...")
        return source_files

    def create_list_of_tuples(self):
        files = self.source_files
        text = self.pages_list
        return list(zip(files, text))


def func_json_to_dict(response):
    return json.loads(response.additional_kwargs['function_call']['arguments'])



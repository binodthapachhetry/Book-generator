BOOK_TEXT_PROMPT = """
Write an engaging, great 10 page children's picture book. Each page should have 2-3 sentences. There should be rhymes.
We will be adding pictures of the environment/scenery for each page, so pick a pretty setting/place. Limit of 10 pages,
do not exceed 3 sentences per page. Do not exceed 10 pages.

Before the story begins, write a "Page 0: {title}" page. The title should be the name of the book, no more than four words.


Format like: Page 0: {title}, Page 1: {text}, etc. Do not write anything else. 
"""

get_visual_description_function = [{
    'name': 'get_passage_setting',
    'description': 'Enhance the passage into a detailed visual description for image generation. Focus on converting narrative to visual elements while MAINTAINING CHARACTER CONSISTENCY. Preserve key actions and characters EXACTLY as described in character references.',
    'parameters': {
        'type': 'object',
        'properties': {
            'enhanced_visual': {
                'type': 'string',
                'description': 'Enhanced visual description directly usable as SD prompt',
            }
        },
        'required': ['enhanced_visual']
    }
}]

get_character_reference_function = [{                                                                                                                                     
    'name': 'get_character_reference',                                                                                                                                    
    'description': 'Extract and define CONSISTENT visual attributes for all characters. If the book text does not specify an attribute, you MUST invent one that fits the story. MUST include concrete details:',                                                                                                                                   
    'parameters': {                                                                                                                                                       
        'type': 'object',                                                                                                                                                 
        'properties': {                                                                                                                                                   
            'character_descriptions': {                                                                                                                                   
                'type': 'string',                                                                                                                                         
                'description': (                                                                                                                                          
                    'FOR EACH CHARACTER SPECIFY (invent if not provided in the story):\n'                                                                                 
                    '- Full name\n'                                                                                                                                       
                    '- Exact age or age range\n'                                                                                                                          
                    '- Hair: color, length, style, and any accessories (e.g. "blonde pigtails with red ribbon")\n'                                                        
                    '- Eyes: color (e.g. "green eyes")\n'                                                                                                                 
                    '- Clothing: detailed description of typical outfit (e.g. "yellow sundress with blue polka dots")\n'                                                  
                    '- Height/build: in absolute terms (e.g. "3 feet tall") or relative to another character (e.g. "taller than Alex")\n'                                 
                    'EXAMPLE: "June: 5 years old, blonde pigtails with red ribbon, green eyes, yellow sundress with blue polka dots, 3.5 feet tall. Alex: 3 years old,short curly brown hair, blue eyes, striped blue overalls, 2.5 feet tall."'                                                                                                
                )                                                                                                                                                         
            }                                                                                                                                                             
        },                                                                                                                                                                
        'required': ['character_descriptions']                                                                                                                            
    }                                                                                                                                                                     
}]  

get_lighting_and_atmosphere_function = [{
    'name': 'get_lighting_and_atmosphere',
    'description': 'Generate a  highly detailed visual description of the overall atmosphere and color palette of a book',
    'parameters': {
        'type': 'object',
        'properties': {
            'lighting': {
                'type': 'string',
                'description': 'The lighting atmosphere of the book, eg. cheerful atmosphere',
            },
            'mood': {
                'type': 'string',
                'description': 'The mood of the book, eg. lively mood',
            },
            'color_palette': {
                'type': 'string',
                'description': 'The color palette of the book, eg. bright and vivid color palette',
            },
        },
        'required': ['lighting', 'mood', 'color_palette']
    }
}]

import os

from dotenv import load_dotenv
import streamlit as st

from api_utils import BuildBook
from deep_lake_utils import SaveToDeepLake
from pdf_gen_utils import build_pdf

STYLES = {
    'Whimsical': 'childrens book illustration style, soft watercolor, friendly cartoon animals, bright primary colors, simple shapes, sparkles, smiling suns, chubby clouds, oversized flowers, happy faces, crayon-like textures, gentle gradients, minimal shading, white outlines, Disney Junior style, PBS Kids aesthetic'
}

load_dotenv('keys.env')
dataset_path = os.getenv('DATASET_PATH')


def main():
    st.title("Book Generator 📚")
    user_input = st.text_input("Enter a prompt to generate a picture book based off of!", max_chars=250)
    style = st.selectbox("Select a style for your picture book!", [key for key in STYLES.keys()])
    model = st.radio("Select a model to use", ['gpt-4.1-2025-04-14'])
    # deep_lake = st.checkbox("Save to Deep Lake?")
    if 'not_saving' not in st.session_state:
        st.session_state['not_saving'] = True
    if st.button('Generate!') and user_input and st.session_state['not_saving']:
        with st.spinner('Generating your book...'):
            build_book = BuildBook(model, user_input, f'{STYLES[style]}')
            
            # Display debug info
            st.subheader("Debug: Page Text to SD Prompts")
            for i, item in enumerate(build_book.debug_info):
                with st.expander(f"Page {i+1}"):
                    st.write("**Original Text:**")
                    st.write(item['page_text'])
                    st.write("**Enhanced Visual Description:**")
                    st.write(item['enhanced_visual'])
                    st.write("**Final SD Prompt:**")
                    st.code(item['final_prompt'])
            
            pages = build_book.list_of_tuples
            finished_pdf = build_pdf(pages, 'result.pdf')
            file_bytes = open(finished_pdf, 'rb').read()
            st.download_button(label='Download Book', data=file_bytes, file_name='picture_book.pdf',
                               key='download_button')
            st.write('Your book has been generated! Click the download button to download it. It is also saved'
                     'in the project directory.')
        # if deep_lake and st.session_state['not_saving']:
        #     st.session_state['not_saving'] = False
        #     with st.spinner('Saving to DeepLake...'):
        #         try:
        #             SaveToDeepLake(build_book, dataset_path=dataset_path).fill_dataset()
        #             st.markdown(
        #                 f'Your images and SD prompts have been saved to Deep Lake! [View it here](https://app.activeloop.ai/datasets/mydatasets/)')
        #             st.session_state['not_saving'] = True

        #         except:
        #             st.write(
        #                 'There was an error saving to Deep Lake. Ensure your API key and dataset path are correct, then try again.')
        #             st.session_state['not_saving'] = True


if __name__ == '__main__':
    main()

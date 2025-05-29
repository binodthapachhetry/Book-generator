BOOK_TEXT_PROMPT = """
Write an engaging, great 3-6 page children's picture book. Each page should have 2-3 sentences. There should be rhymes.
We will be adding pictures of the environment/scenery for each page, so pick a pretty setting/place. Limit of 7 pages,
do not exceed 3 sentences per page. Do not exceed 7 pages.

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
    'description': 'Extract and define CONSISTENT visual attributes for all characters. MUST include concrete details:',
    'parameters': {
        'type': 'object',
        'properties': {
            'character_descriptions': {
                'type': 'string',
                'description': (
                    'FOR EACH CHARACTER SPECIFY:\n'
                    '- Exact hair color/length/style (e.g. "brown pigtails with red ribbon")\n'
                    '- Precise eye color (e.g. "green eyes")\n'
                    '- Detailed clothing (e.g. "yellow sundress with blue polka dots")\n'
                    '- Fixed height/build (e.g. "June is 1.2x taller than Alex")\n'
                    'EXAMPLE: "June: 5yo, brown pigtails, green eyes, yellow sundress. Alex: 3yo, blonde curls, blue eyes, striped overalls. June is 1.3x taller than Alex"'
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

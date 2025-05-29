BOOK_TEXT_PROMPT = """
Write an engaging, great 3-6 page children's picture book. Each page should have 2-3 sentences. There should be rhymes.
We will be adding pictures of the environment/scenery for each page, so pick a pretty setting/place. Limit of 7 pages,
do not exceed 3 sentences per page. Do not exceed 7 pages.

Before the story begins, write a "Page 0: {title}" page. The title should be the name of the book, no more than four words.


Format like: Page 0: {title}, Page 1: {text}, etc. Do not write anything else. 
"""

get_visual_description_function = [{
    'name': 'get_passage_setting',
    'description': 'Generate a highly detailed visual description of a story passage including characters, actions, and setting',
    'parameters': {
        'type': 'object',
        'properties': {
            'characters': {
                'type': 'string',
                'description': 'Main characters in the scene including their appearance, emotions, and actions',
            },
            'key_action': {
                'type': 'string',
                'description': 'The primary action happening in the scene',
            },
            'base_setting': {
                'type': 'string',
                'description': 'General location (e.g. forest, village)',
            },
            'setting': {
                'type': 'string',
                'description': 'The detailed visual setting of the passage, e.g. a snowy mountain village',
            },
            'time_of_day': {
                'type': 'string',
                'description': 'The time of day of the passage, e.g. nighttime, daytime, dawn.',
            },
            'weather': {
                'type': 'string',
                'description': 'The weather of the passage, eg. heavy rain with dark clouds.',
            },
            'specific_details': {
                'type': 'string',
                'description': 'Background objects and atmospheric details of the passage.',
            }
        },
        'required': ['characters', 'key_action', 'base_setting', 'setting']
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

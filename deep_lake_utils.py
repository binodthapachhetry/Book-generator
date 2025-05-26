import os

import deeplake
from dotenv import load_dotenv

load_dotenv('keys.env')


class SaveToDeepLake:
    def __init__(self, buildbook_instance, dataset_path=None):
        self.dataset_path = dataset_path
        
        # Check if ACTIVELOOP_TOKEN is set
        activeloop_token = os.getenv('ACTIVELOOP_TOKEN')
        if activeloop_token and activeloop_token != 'token here':
            os.environ['ACTIVELOOP_TOKEN'] = activeloop_token
        
        try:
            self.ds = deeplake.load(dataset_path, read_only=False)
            self.loaded = True
        except Exception as e:
            print(f"Note: {e}")
            self.ds = deeplake.empty(dataset_path)
            self.loaded = False

        self.prompt_list = buildbook_instance.sd_prompts_list
        self.images = buildbook_instance.source_files

    def fill_dataset(self):
        if not self.loaded:
            self.ds.create_tensor('prompts', htype='text')
            self.ds.create_tensor('images', htype='image', sample_compression='png')
        for i, prompt in enumerate(self.prompt_list):
            self.ds.append({'prompts': prompt, 'images': deeplake.read(self.images[i])})

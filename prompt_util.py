'''
yaml -> 인덱스 테이블 업데이트
'''
import os
import yaml
import json
import pandas as pd
from __config__ import PPT_FPATH, RESULT_FPATH


class ConfigControler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.config = self.load_config()
        self.index_table = pd.read_csv(PPT_FPATH)

    def load_config(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)

    def update_prompt_info(self):
        new_row = {
            'prompt_ver': self.config['prompt_ver'],
            'model': self.config.get('model', 'llama-3.1-sonar-large-128k-online'),
            'summary': self.config.get('summary', ''),
            'file_name': self.file_path
        }
        self.index_table = pd.concat([self.index_table, pd.DataFrame([new_row])], ignore_index=True)
        self.index_table.to_csv(PPT_FPATH, index=False)

    def save_result(self, fname:str, test_results:list[dict]):
        base_fname = fname + '_'
        existing_files = [f for f in os.listdir(RESULT_FPATH) if f.startswith(base_fname)]
        max_index = 0
        
        for file in existing_files:
            try:
                current_index = int(file[len(base_fname):-5])  # -5 to remove '.json'
                max_index = max(max_index, current_index)
            except ValueError:
                continue
        
        for idx, result in enumerate(test_results):
            json_fname = base_fname + str(max_index + idx + 1) + '.json'
            file_path = os.path.join(RESULT_FPATH, json_fname)
            with open(file_path, 'w', encoding='utf-8') as json_file:
                json.dump(result, json_file, ensure_ascii=False, indent=4)


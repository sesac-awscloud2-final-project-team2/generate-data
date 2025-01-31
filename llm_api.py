'''
perplexity search 결과 반환 클래스
'''

import json
import requests
import os
from dotenv import load_dotenv
import re
load_dotenv()

class SearchPrompt:
    def __init__(self, model_dict:dict):
        self.api_key = os.getenv('PERPLEXITY_KEY')
        self.config = model_dict
        self.url = "https://api.perplexity.ai/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def preprocess_response(self, response:str) -> list:
        # 정규식을 사용하여 문자열의 이스케이프된 문자를 처리
        response = re.sub(r'``', '', response)  # 개행 문자 제거
        response = re.sub(r'\\n', '', response)  # 개행 문자 제거
        response = re.sub(r'\\\'', "'", response)  # 이스케이프된 작은따옴표 처리
        response = re.sub(r'\\\"', '"', response)  # 이스케이프된 큰따옴표 처리
        response = response.replace('\n', '')  # 모든 개행 문자 제거

        json_objects = re.findall(r'\{.*?\}', response)

        if json_objects:
            result_list = [json.loads(obj) for obj in json_objects]
        else:
            result_list = [{}]
        return result_list

    def get_type_json_file(self, type:str):
        with open(f'{type}.json', 'r') as f:
            type_json = json.load(f)
            type_str = json.dumps(type_json, ensure_ascii=False)
        return type_str

    def stack_logs(self, e, pre_result, type_name):
        import os

        # logs 폴더가 없으면 생성
        if not os.path.exists('logs'):
            os.makedirs('logs')

        # logs 폴더 내의 파일 목록을 가져와서 가장 큰 번호를 찾음
        log_files = [f for f in os.listdir('logs') if f.endswith('_log.txt')]
        if log_files:
            latest_log_num = max([int(f.split('_')[0]) for f in log_files])
            new_log_num = latest_log_num + 1
        else:
            new_log_num = 1

        # 새로운 로그 파일 이름 생성
        log_file_name = f'logs/{new_log_num}_log.txt'

        # self.headers와 pre_result를 텍스트로 변환하여 저장
        with open(log_file_name, 'w', encoding='utf-8') as log_file:
            log_file.write("type:\n")
            log_file.write(type_name)
            log_file.write("\n\nPre_result:\n")
            log_file.write(str(pre_result))
            log_file.write("\n\nError MSG:\n")
            log_file.write(str(e))

    def generate_data(self, type_name:str) -> dict:
        messages = [
            {
                "role": "system", 
                "content": self.config['role']['system']['content']
            },
            {
                "role": "user",
                "content": self.config['role']['user']['content'] + self.get_type_json_file('prompt/'+type_name)
            }
        ]
        
        payload = {
            "model": self.config.get('model', 'llama-3.1-sonar-large-128k-online'),
            "messages": messages,
            "temperature": self.config.get('temperature', 0.3),
            "max_tokens": self.config.get('max_tokens', 2000),
            "top_p": self.config.get('top_p', 0.9),
            "frequency_penalty": self.config.get('frequency_penalty', 1.0),
            "presence_penalty": self.config.get('presence_penalty', 0.0),
            "search_domain_filter": self.config.get('search_domain_filter', None),
            "return_images": self.config.get('return_images', False),
            "return_related_questions": self.config.get('return_related_questions', False),
            "search_recency_filter": self.config.get('search_recency_filter', None),
            "top_k": self.config.get('top_k', 0)
        }

        response = requests.post(self.url, json=payload, headers=self.headers).json()
        pre_result = response['choices'][0]['message']['content']
        
        try:
            result_list = self.preprocess_response(pre_result)
            # result_dict['prompt_ver'] = self.config.get('prompt_ver')
        except Exception as e:
            self.stack_logs(e, pre_result, type_name)
            result_list = [{}]
        return result_list

import sys
from llm_api import SearchPrompt
from prompt_util import ConfigControler

def main(yaml_file_path, type_name, save_fname:str):
    save_fname = save_fname.split('/')[-1]
    config_controller = ConfigControler(yaml_file_path)
    search_prompt = SearchPrompt(config_controller.config)

    result_list = search_prompt.generate_data(type_name)
    config_controller.update_prompt_info()
    config_controller.save_result(save_fname, result_list)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python __run__.py <yaml 파일 경로> <샘플명 (join, trip, experience)>")
        sys.exit(1)
    yaml_file_path = sys.argv[1]
    type_name = sys.argv[2]
    # yaml_file_path = 'prompt/prompt_3.yaml'
    # type_name = 'join'
    main(yaml_file_path, type_name, yaml_file_path.replace('.yaml', ''))
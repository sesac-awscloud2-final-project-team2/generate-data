import sys
from llm_api import SearchPrompt
from prompt_util import ConfigControler

def experience(yaml_file_path, save_fname, trip_json_fname):
    save_fname = save_fname.split('/')[-1]
    config_controller = ConfigControler(yaml_file_path)
    search_prompt = SearchPrompt(config_controller.config)

    result_list = search_prompt.generate_data(type_name, trip_json_fname)
    config_controller.update_prompt_info()
    config_controller.save_result(save_fname, result_list)

def main(yaml_file_path, type_name, save_fname:str):
    save_fname = save_fname.split('/')[-1]
    config_controller = ConfigControler(yaml_file_path)
    search_prompt = SearchPrompt(config_controller.config)

    result_list = search_prompt.generate_data(type_name)
    config_controller.update_prompt_info()
    config_controller.save_result(save_fname, result_list)

if __name__ == "__main__":
    # if len(sys.argv) < 2:
    #     print("사용법: python __run__.py <yaml 파일 경로> <샘플명 (join, trip, experience)> <experience일 경우에 trip json 파일경로>")
    #     sys.exit(1)
    # yaml_file_path = sys.argv[1]
    # type_name = sys.argv[2]
    yaml_file_path = 'prompt/exp_prompt_1.yaml'
    save_fname = yaml_file_path.replace('.yaml', '')
    type_name = 'experience'
    trip_json_file ='logs/trip/prompt_1_1.json'

    if type_name == 'experience':
        # trip_json_file = sys.argv[3]
        experience(yaml_file_path, save_fname, trip_json_file)
    else:
        main(yaml_file_path, type_name, save_fname)
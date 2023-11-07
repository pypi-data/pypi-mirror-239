from abstract_ai import SaveManager,get_any_value,safe_json_loads
files = """C:/Users/jrput/Documents/python projects/Modules/test_modules/test_abstract_test_ai/response_data/2023-11-05/gpt-4-0613/1699214399.json
C:/Users/jrput/Documents/python projects/Modules/test_modules/test_abstract_test_ai/response_data/2023-11-05/gpt-4-0613/1699214352.json
C:/Users/jrput/Documents/python projects/Modules/test_modules/test_abstract_test_ai/response_data/2023-11-05/gpt-4-0613/1699214319.json
C:/Users/jrput/Documents/python projects/Modules/test_modules/test_abstract_test_ai/response_data/2023-11-05/gpt-4-0613/1699214257.json
C:/Users/jrput/Documents/python projects/Modules/test_modules/test_abstract_test_ai/response_data/2023-11-05/gpt-4-0613/1699214198.json
C:/Users/jrput/Documents/python projects/Modules/test_modules/test_abstract_test_ai/response_data/2023-11-05/gpt-4-0613/1699214175.json
C:/Users/jrput/Documents/python projects/Modules/test_modules/test_abstract_test_ai/response_data/2023-11-05/gpt-4-0613/1699213848.json
C:/Users/jrput/Documents/python projects/Modules/test_modules/test_abstract_test_ai/response_data/2023-11-05/gpt-4-0613/1699213714.json
C:/Users/jrput/Documents/python projects/Modules/test_modules/test_abstract_test_ai/response_data/2023-11-05/gpt-4-0613/1699214528.json
C:/Users/jrput/Documents/python projects/Modules/test_modules/test_abstract_test_ai/response_data/2023-11-05/gpt-4-0613/1699214505.json
C:/Users/jrput/Documents/python projects/Modules/test_modules/test_abstract_test_ai/response_data/2023-11-05/gpt-4-0613/1699214471.json
C:/Users/jrput/Documents/python projects/Modules/test_modules/test_abstract_test_ai/response_data/2023-11-05/gpt-4-0613/1699214440.json""".split('\n')
import json
for each in files:
    data = SaveManager.read_saved_json(each)
    content = get_any_value(data['response'],'content')
    if isinstance(content,str):
        content = json.loads(content.replace('False','false').replace("True",'true'))
    if isinstance(content,dict):
        
        input(content['api_response'])

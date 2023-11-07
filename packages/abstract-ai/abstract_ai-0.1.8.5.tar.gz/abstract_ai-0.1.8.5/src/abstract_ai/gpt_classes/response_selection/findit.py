import re
import json

def preprocess_string(s):
    # Replace \" with a unique marker
    s = s.replace('\\"', '*<d<*')
    # Replace any remaining " with '
    s = s.replace('"', "'")
    # Replace the original single quotes (now all are delimiters) with "
    s = s.replace("'", '"')
    # Replace the unique markers back to \"
    s = s.replace('*<d<*', '\\"')
    return s

def postprocess_string(s):
    # After loading the JSON and processing it, if you need to output the JSON
    # or parts of it as a string with the original quote characters, do the reverse.
    s = s.replace('\\"', '*<d<*')
    s = s.replace('"', "'")
    s = s.replace("*<d<*", '\\"')
    return s

def if_key_in_value(data, key):
    if isinstance(data, dict):
        for k, v in data.items():
            if k == key:
                return True
            if isinstance(v, (dict, list)):
                if if_key_in_value(v, key):
                    return True
    elif isinstance(data, list):
        for item in data:
            if if_key_in_value(item, key):
                return True
    return False

def get_path_to_key(data, key, path=None):
    if path is None:
        path = []
    if isinstance(data, dict):
        for k, v in data.items():
            new_path = path + [k]
            if k == key:
                return new_path
            if isinstance(v, (dict, list)):
                found_path = get_path_to_key(v, key, new_path)
                if found_path:
                    return found_path
    elif isinstance(data, list):
        for idx, item in enumerate(data):
            new_path = path + [idx]
            if isinstance(item, (dict, list)):
                found_path = get_path_to_key(item, key, new_path)
                if found_path:
                    return found_path
    return None

def convert_and_find_key(data, key):
    if not isinstance(data, (dict, list)):
        data = preprocess_string(data)
        try:
            data = json.loads(data)
        except json.JSONDecodeError as e:
            print(f"JSON decoding failed: {e}")
            return None, None

    if if_key_in_value(data, key):
        path = get_path_to_key(data, key)
        return path, get_value_from_path(data, path)
    else:
        return None, None

def get_value_from_path(data, path):
    for key in path:
        data = data[key] if isinstance(data, dict) else data[int(key)]
    return data

# Example Usage
from ResponseBuilder import SaveManager
save_mgr = SaveManager()
output = save_mgr.read_saved_json(file_path="C:/Users/jrput/Documents/python projects/Modules/test_modules/test_abstract_test_ai/response_data/2023-11-05/gpt-4-0613/1699175901.json")['response']
input(str(output).split('api_response')[1])

path, value = convert_and_find_key(output, 'api_response')
if path is not None:
    print(f"Path to '{key_to_find}': {path}")
    print(f"Value at path: {value}")
else:
    print(f"Key '{key_to_find}' not found")

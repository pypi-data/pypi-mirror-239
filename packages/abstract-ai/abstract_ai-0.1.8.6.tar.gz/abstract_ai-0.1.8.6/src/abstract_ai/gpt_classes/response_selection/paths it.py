import os
import re
import json
from abstract_utilities.json_utils import get_value_from_path,get_any_value,safe_json_loads
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
def get_any_value_converter(output,key,return_dict=False):
    return_desired_dict=False
    # Preprocess the string to temporarily replace quotes
    if isinstance(output,dict):
        if return_dict:
            return output
        return output[key]
    json_ready_string = preprocess_string(output)
    try:
        # Load the string as a JSON object
        data_json = json.loads(json_ready_string)
        data_json=data_json
        value = get_any_value(data_json,key)
        # Example of processing and then converting back to a string
        output_string = json.dumps(value, indent=4)
        output_string=postprocess_string(output_string)
        return_desired_dict=data_json
    except json.JSONDecodeError as e:
        # Handle JSON errors
        print("Decoding JSON has failed:", e)
    if return_dict and return_desired_dict:
        return return_desired_dict
    return output_string
def find_paths_to_key_in_string(data, key, current_path=None, paths=None):
    if paths is None:
        paths = []
    if current_path is None:
        current_path = []
    if isinstance(data, dict):
        for k, v in data.items():
            new_path = current_path + [k]
            if k == key:
                paths.append(new_path)
            if isinstance(v, (dict, list, str)):
                find_paths_to_key_in_string(v, key, new_path, paths)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            new_path = current_path + [i]
            if isinstance(item, (dict, list, str)):
                find_paths_to_key_in_string(item, key, new_path, paths)
    elif isinstance(data, str):
        # Preprocess string to replace problematic quotes
        processed_string = preprocess_string(data)
        try:
            # Attempt to convert the string to JSON and search within it
            json_data = json.loads(processed_string)
            find_paths_to_key_in_string(json_data, key, current_path, paths)
        except json.JSONDecodeError:
            # If decoding fails, check if the string itself contains the key
            if key in data:
                paths.append(current_path)
    return paths
def get_value_from_object(data=None,key_to_find=None):
    save_mgr = SaveManager()
    dict_values=[]
    if isinstance(data,str):
        if os.path.exists(data):
            data=save_mgr.read_saved_json(file_path=data)
    data=safe_json_loads(data)
    value = get_any_value(data,key_to_find)
    paths = find_paths_to_key_in_string(data,key_to_find)
    for path in paths:
        string_value = get_value_from_path(data,path[:-1])
        dict_values.append(get_any_value_converter(string_value,key_to_find,return_dict=True))
    return dict_values
from ResponseBuilder import SaveManager
input(get_value_from_object("C:/Users/jrput/Documents/python projects/Modules/test_modules/test_abstract_test_ai/response_data/2023-11-05/gpt-4-0613/1699175901.json",'api_response'))

import json

import os

def load_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_json_file(data, filepath):
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

def deep_merge(dict1, dict2):
    for key in dict2:
        if key in dict1:
            if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
                deep_merge(dict1[key], dict2[key])
            else:
                dict1[key] = dict2[key]
        else:
            dict1[key] = dict2[key]

# Load the JSON files
qa_data_file = r'C:\Projects\chatbot\merged_qa_data.json'
qa_server2_file = r'C:\Projects\chatbot\windows.json'

qa_data = load_json_file(qa_data_file)
qa_server2 = load_json_file(qa_server2_file)

# Merge the JSON data
deep_merge(qa_data, qa_server2)

# Save the merged JSON data
merged_file_path = r'C:\Projects\chatbot\qa_data.json'
save_json_file(qa_data, merged_file_path)

print(f"Merged file saved at {merged_file_path}")

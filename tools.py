import json


def from_dict_to_json(data, file_name):
     with open(file_name, 'w', encoding='utf-8') as f:
         json.dump(data, f, ensure_ascii=False, indent=5)

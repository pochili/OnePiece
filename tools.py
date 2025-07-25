import json

def from_dict_to_json(data, file_name):
     with open(file_name, 'w', encoding='utf-8') as f:
         json.dump(data, f, ensure_ascii=False, indent=5)


def from_json_to_dict(file_name):
    """Load a list of dictionaries from a JSON file."""
    with open(file_name, 'r', encoding='utf-8') as f:
        return json.load(f)
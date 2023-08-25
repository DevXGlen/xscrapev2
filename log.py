import json

def update_log(json_fpath, new_data):
    with open(json_fpath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    data.append(new_data)

    with open(json_fpath, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)
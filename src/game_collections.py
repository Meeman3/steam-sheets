import os, json, re
from dotenv import load_dotenv

def get_steam_json(id: str | None = None, path_to_json = None):
    if path_to_json == None:
        if id == None:
            raise SystemExit("Need either ID or path to json")

        path_to_json = f"/mnt/c/Program Files (x86)/Steam/userdata/{id}/config/cloudstorage/cloud-storage-namespace-1.json"
        
    with open(path_to_json, "r") as p:
        steam_json = json.load(p)
    
    collections_dict = {}
    
    for pair in steam_json:
        if not (isinstance(pair, list) and len(pair) == 2):
            continue

        pair_dict = pair[1]
        if not isinstance(pair_dict, dict):
            continue

        list_value = pair_dict.get("value")
        if not isinstance(list_value, str):
            continue
        
        try:
            decoded_list = json.loads(list_value)
        except json.JSONDecodeError:
            continue

        if not isinstance(decoded_list, dict):
            continue

        name = decoded_list.get("name")
        added = decoded_list.get("added", [])

        if name:
            collections_dict[name] = added

    
    return collections_dict

def invert_collections(collections_dict):
    inverted_dict = {}

    for key in collections_dict:
        for id in collections_dict[key]:
            if id in inverted_dict:
                inverted_dict[id].append(key)
            else:
                inverted_dict[id] = [key]
    
    return inverted_dict



load_dotenv()
    
collections_dict = get_steam_json(id = os.getenv("STEAM_ID3_NUM"))

print(invert_collections(collections_dict))


    
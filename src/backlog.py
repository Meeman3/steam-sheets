import json
from hltb import game_add_hltb

def get_backlog_ids(*args):
    backlog_ids = []

    with open("data/all_collections.json", "r") as collections:
        collection_json = json.load(collections)
    
    with open("data/collections_lists.json", "r") as id:
        lists_json = json.load(id)

    for arg in args:
        if arg not in collection_json:
            raise Exception(f"{arg} not a valid collection")
    
        backlog_ids.extend(lists_json[f"{arg}"])
    
    with open("data/backlog_ids.json", "w") as back:
        json.dump(backlog_ids, back, ensure_ascii=False, indent=3)
    
    return backlog_ids


def backlog_ids_to_dicts(backlog_ids):
    backlog_games_dicts = []

    with open("data/owned_games.json", "r") as owned:
        owned_json = json.load(owned)

    for id in backlog_ids:
        for dict in owned_json:
            if id == dict["appid"]:
                dict = game_add_hltb(dict)
                backlog_games_dicts.append(dict)
                
            
    with open("data/backlog_games.json", "w") as back:
        json.dump(backlog_games_dicts, back, ensure_ascii=False, indent=3)

    return backlog_games_dicts

backlog_ids_to_dicts(get_backlog_ids("Backlog"))





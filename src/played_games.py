import json

def get_played_games(Hidden = False, software = False, *args):
    played_games = []

    with open("data/owned_games.json", "r") as owned:
        owned_json = json.load(owned)

    with open("data/ids_with_collections.json", "r") as collections:
        collections_json = json.load(collections)

    for game in owned_json:
        blacklist = False
        for arg in args:
            if f"{game["appid"]}" in collections_json:
                if arg in collections_json[f"{game["appid"]}"]:
                    blacklist = True
                if Hidden == False and "Hidden" in collections_json[f"{game["appid"]}"]:
                    blacklist = True
                if software == False and "software" in collections_json[f"{game["appid"]}"]:
                    blacklist = True

        if game["rtime_last_played"] != 0 and blacklist == False:
            played_games.append(game)
    
    with open("data/played.json", "w") as played:
        json.dump(played_games, played, ensure_ascii=False, indent=3)

    return played_games

get_played_games()
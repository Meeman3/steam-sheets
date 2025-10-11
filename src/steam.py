import os, json, requests
from dotenv import load_dotenv

Owned_Games_API = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"

def get_owned_games(steam_key: str, steam_id: str, include_appinfo = True, include_free = False):
    params = {
        "key": steam_key,
        "steamid": steam_id,
        "include_appinfo": include_appinfo,
        "include_played_free_games": include_free
    }

    get_info = requests.get(Owned_Games_API, params= params, timeout=20)
    get_info.raise_for_status()

    data = get_info.json().get("response", {})
    game_dicts = data.get("games", [])
    

    return game_dicts

def my_owned_games():
    load_dotenv()
    key = os.getenv("STEAM_API_KEY")
    id = os.getenv("STEAM_ID64")

    if not key or not id:
        raise SystemExit("set STEAM_API_KEY and STEAM_ID64 in .env")
    
    games = get_owned_games(key, id)

    os.makedirs("data", exist_ok=True)
    with open("data/owned_games.json", "w") as owned:
        json.dump(games, owned, ensure_ascii=False, indent=3)
        
        

my_owned_games()   
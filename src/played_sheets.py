from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from dotenv import load_dotenv
import os
import json

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
load_dotenv()
played_id = os.getenv("PLAYED_ID")

def get_creds():
    creds = None
    if os.path.exists("creds/token.json"):
        creds = Credentials.from_authorized_user_file("creds/token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())  # silent refresh
        else:
            flow = InstalledAppFlow.from_client_secrets_file("creds/credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)  # one-time consent
        with open("creds/token.json", "w") as token:
            token.write(creds.to_json())
    return creds

creds = get_creds()
sheet = build("sheets", "v4", credentials=creds).spreadsheets()

def write_played(game_dict, read_values):

    if read_values == []:
        sheet.values().update(
            spreadsheetId=f"{played_id}",
            range=f"Sheet1!A1:E1",
            valueInputOption="RAW",
            body={"values": [["Game", "Completed?",	"Play Time", "Play Period?", "Rating", "Date Finished", "100%?", "Thoughts?"]]},
        ).execute()

        read_values = [["Game", "Completed?", "Play Time", "Play Period?", "Rating", "Date Finished", "100%?", "Thoughts?"]]
    
    if game_dict == None:
        return
    else:

        game_name = game_dict.get("name").strip()
        stripped_name = game_name.lower()
        playtime = (game_dict["playtime_windows_forever"] 
        + game_dict["playtime_mac_forever"] 
        + game_dict["playtime_linux_forever"] 
        + game_dict["playtime_deck_forever"])/60
        
        with open("data/ids_with_collections.json") as idc:
            collections_json = json.load(idc)
        
        game_collections = collections_json.get(f"{game_dict['appid']}")
            
        completed_game = "No"
        p100 = "No"
        
        if game_collections:
            if "multiplayer" in game_collections:
                if "completed" not in game_collections:
                    completed_game = "Multiplayer"
                    p100 = "N/A"
                    
            if "Dropped" in game_collections:
                completed_game = "Dropped"
                
            if "completed" in game_collections:
                completed_game = "Yes"
                
            if "100%" in game_collections:
                p100 = "Yes"
                
        
        duplicate = None
        for i, row in enumerate(read_values, start=1):
            if row:
                cell = str(row[0]).strip().lower()
            if cell == stripped_name:
                duplicate = i
                break
    
        game_body = [game_name,
                    completed_game,
                    round(playtime, 2),
                    "N/A",
                    "N/A",
                    "N/A",
                    p100]
        
        game_body_str = [game_name,
                    completed_game,
                    str(round(playtime, 2)),
                    "N/A",
                    "N/A",
                    "N/A",
                    p100]
    

        if duplicate is not None:
            if game_body_str in read_values:
                return
            else:
                sheet.values().update(
                    spreadsheetId=f"{played_id}",
                    range=f"Sheet1!A{duplicate}:G{duplicate}",
                    valueInputOption="RAW",
                    body={"values": [game_body]},
                ).execute()
            return
            

        else:
            sheet.values().append(
                spreadsheetId=f"{played_id}",
                range="Sheet1!A:E",
                valueInputOption="RAW",
                insertDataOption="INSERT_ROWS",
                body={"values": [game_body]},
            ).execute()
            return


def read_played():
    resp = sheet.values().get(
        spreadsheetId=f"{played_id}",
        range="Sheet1",
    ).execute()
    return resp


with open("data/played.json", "r") as played:
            played_json = json.load(played)
            
values = read_played().get("values", [])
for game_dict in played_json:
    write_played(game_dict, read_values=values)
    

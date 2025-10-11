from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from dotenv import load_dotenv
import os
import json

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
load_dotenv()
backlog_id = os.getenv("BACKLOG_ID")

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

def write_backlog(game_dict, read_values):

    if read_values == []:
        sheet.values().update(
            spreadsheetId=f"{backlog_id}",
            range=f"Sheet1!A1:E1",
            valueInputOption="RAW",
            body={"values": [["Game", "Anticipation", "HLTB?", "Owned?", "Status"]]},
        ).execute()

        read_values = [["Game", "Anticipation", "HLTB?", "Owned?", "Status"]]
    
    if game_dict == None:
        return
    else:
        game_name = game_dict.get("name").strip()
        stripped_name = game_name.lower()
        
        with open("data/ids_with_collections.json") as idc:
            collections_json = json.load(idc)
        
        game_collections = collections_json.get(f"{game_dict['appid']}")
        
        status = "N/A"
        if game_collections:
            if "multiplayer" in game_collections:
                if "completed" not in game_collections:
                    status = "Multiplayer"
                    
            if "Dropped" in game_collections:
                status = "Dropped"
                
            if "completed" in game_collections:
                status = "Completed"
                
            if "100%" in game_collections:
                status = "Completed"

        game_body = [game_name,
                    "N/A",
                    game_dict['hltb'],
                    "Yes",
                    status]
        
        
        duplicate = None
        for i, row in enumerate(read_values, start=1):
            if row:
                cell = str(row[0]).strip().lower()
            if cell == stripped_name:
                duplicate = i
                break

        if duplicate is not None:
            if game_body in read_values:
                return
            else:
                sheet.values().update(
                    spreadsheetId=f"{backlog_id}",
                    range=f"Sheet1!A{duplicate}:E{duplicate}",
                    valueInputOption="RAW",
                    body={"values": [game_body]},
                ).execute()
            return
            

        else:
            sheet.values().append(
                spreadsheetId=f"{backlog_id}",
                range=f"Sheet1!A:E",
                valueInputOption="RAW",
                insertDataOption="INSERT_ROWS",
                body={"values": [game_body]},
            ).execute()
            return


def read_backlog():
    resp = sheet.values().get(
        spreadsheetId=f"{backlog_id}",
        range="Sheet1!A:D",
    ).execute()
    return resp


with open("data/backlog_games.json", "r") as backlog:
            backlog_json = json.load(backlog)

values = read_backlog().get("values", [])
for game_dict in backlog_json:
    write_backlog(game_dict, read_values=values)
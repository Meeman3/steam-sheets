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

def write_backlog(game_id=None):
    values = read_backlog().get("values", [])

    if values == []:
        sheet.values().update(
            spreadsheetId=f"{backlog_id}",
            range=f"Sheet1!A1:E1",
            valueInputOption="RAW",
            body={"values": [["Game", "Anticipation", "HLTB?", "Owned?", "Status"]]},
        ).execute()

        values = [["Game", "Anticipation", "HLTB?", "Owned?", "Status"]]
    
    if game_id == None:
        return
    else:
        with open("data/backlog_games.json", "r") as backlog:
            backlog_json = json.load(backlog)


        

        for game_dict in backlog_json:
            

            if game_id == game_dict.get("appid"):
                game_name = game_dict.get("name").strip()
                stripped_name = game_name.lower()

                
                values = sheet.values().get(
                        spreadsheetId=backlog_id, range="Sheet1!A:Z", majorDimension="ROWS"
                    ).execute().get("values", [])
                
                duplicate = None
                for i, row in enumerate(values, start=1):
                    if row:
                        cell = str(row[0]).strip().lower()
                    if cell == stripped_name:
                        duplicate = i
                        break

                if duplicate is not None:
                    sheet.values().update(
                        spreadsheetId=f"{backlog_id}",
                        range=f"Sheet1!A{duplicate}:E{duplicate}",
                        valueInputOption="RAW",
                        body={"values": [[game_name, "N/A", game_dict['hltb'], "Yes", "N/A"]]},
                    ).execute()
                    return
                    

                else:
                    sheet.values().append(
                        spreadsheetId=f"{backlog_id}",
                        range=f"Sheet1!A:E",
                        valueInputOption="RAW",
                        insertDataOption="INSERT_ROWS",
                        body={"values": [[game_name, "N/A", game_dict['hltb'], "Yes", "N/A"]]},
                    ).execute()
                    return


def read_backlog():
    resp = sheet.values().get(
        spreadsheetId=f"{backlog_id}",
        range="Sheet1",
    ).execute()
    return resp


with open("data/backlog_games.json", "r") as backlog:
            backlog_json = json.load(backlog)

for game_dict in backlog_json:
    write_backlog(game_dict.get("appid"))
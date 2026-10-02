import json
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

DATA_FILE = "data.json"
app = FastAPI()

class Player(BaseModel):
    name: str
    # id: Optional[int] = None
    club_id: int

class Club(BaseModel):
    name:str
    # club_id: Optional[int] = None

@app.get("/")
def get_all():
    return readData()

@app.post("/add/player")
def add_player(player: Player):
    player_list = get_players()
    if (not hasClub(player.club_id)):
        raise HTTPException(status_code=404, detail="No Club with such id")
    if (not redudancy_check(player.name, player_list)):
        player_dict = player.model_dump()
        player_dict["id"] = giveID(player_list, "id")
        player_list.append(player_dict)
        writePlayer(player_list)
        return player_dict
    else:
        raise HTTPException(status_code=400, detail="Player already exists")

@app.post("/add/club")
def add_club(club: Club):
    club_list = get_club()
    if (not redudancy_check(club.name, club_list)):
        club_dict = club.model_dump()
        club_dict["club_id"] = giveID(club_list, "club_id")
        club_list.append(club_dict)
        writeClub(club_list)
        return club_dict
    else:
        raise HTTPException(status_code=400, detail= "Club already exists")

def readData():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            content = json.load(file)
            return content
    except Exception as e:
        return { Player: [], Club: [] }

def writeData(data: list):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def writePlayer(players: dict):
    current_list = readData()
    current_list["Player"] = players
    writeData(current_list)

def writeClub(clubs: dict):
    current_list = readData()
    current_list["Club"] = clubs
    writeData(current_list)

def giveID(lists: list, key: str):
    ids = [x[key] for x in lists]
    if len(ids) == 0:
        return 1
    else:
        return max(ids) + 1


def redudancy_check(name: str, players: list): 
    player_names = [p["name"] for p in players]
    if name in player_names:
        return True
    return False

def get_players():
    return readData()["Player"]

def get_club():
    return readData()["Club"]

def hasClub(id: int):
    clubs = get_club()
    club_ids = [c["club_id"] for c in clubs]
    if id in club_ids:
        return True
    return False
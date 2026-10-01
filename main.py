import json
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

DATA_FILE = "data.json"
app = FastAPI()

class Player(BaseModel):
    name: str
    # id: Optional[int] = None

@app.get("/")
def get_all():
    return readData()

@app.post("/add")
def add_player(player: Player):
    current_list = readData()
    if (not redudancy_check(player.name)):
        player_dict = player.model_dump()
        player_dict["id"] = giveID(current_list)
        current_list.append(player_dict)
        writeData(current_list)
        return player_dict
    else:
        raise HTTPException(status_code=404, detail="Player already exists")
    
def readData():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            content = json.load(file)
            return content
    except Exception as e:
        return []

def writeData(data: list):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def giveID(players: list):
    player_ids = [p["id"] for p in players]
    if len(player_ids) == 0:
        return 1
    else:
        return max(player_ids) + 1


def redudancy_check(name: str, players: list): 
    player_names = [p["name"] for p in players]
    if name in player_names:
        return True
    return False
    
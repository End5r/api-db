import json
from fastapi import FastAPI
from pydantic import BaseModel

DATA_FILE = "data.json"
app = FastAPI()

class Player(BaseModel):
    name: str
    id: int



@app.get("/")
def get_all():
    return readData()

@app.post("/add")
def add_player(player: Player):
    player_dict = player.model_dump()
    current_list = readData()
    current_list.append(player_dict)
    writeData(current_list)
    return player_dict
    


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
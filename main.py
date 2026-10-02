import json
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

DATA_FILE = "data.json"
app = FastAPI()

class Player(BaseModel):
    name: str
    club_id: int

class Club(BaseModel):
    name:str

@app.delete("/player/{id}")
def delete_player(id: int):
    player_list = get_entities("Player")
    player = getEntity(player_list, id, "id")
    player_list.remove(player) 
    write_entity(player_list, "Player")   
    return {"message": f"Player: {player['name']} was succesfully deleted"}

@app.delete("/club/{club_id}")
def delete_club(club_id: int):
    club_list = get_entities("Club")
    club = getEntity(club_list, club_id, "club_id")
    club_list.remove(club)
    write_entity(club_list, "Club")
    delete_player_club(club_id)

def delete_player_club(club_id: int):
    old_player_list = get_entities("Player")
    new_player_list = [p for p in old_player_list if p["club_id"] != club_id]
    write_entity(new_player_list, "Player") 

@app.get("/player/{id}")
def read_player(id: int):
    player = getEntity(get_entities("Player"), id, "id")
    club = getEntity(get_entities("Club"), player["club_id"], "club_id")

    return {"message": f"{player["name"]} plays at {club["name"]}"}
    
def getEntity(list: list, id: int, key: str):
    for l in list:
        if l[key] == id:
            return l
    raise HTTPException(status_code=404, detail= "Entity not found")

@app.get("/")
def get_all():
    return readData()

@app.post("/add/player")
def add_player(player: Player):
    player_list = get_entities("Player")
    if (not hasClub(player.club_id)):
        raise HTTPException(status_code=404, detail="No Club with such id")
    if (not redudancy_check(player.name, player_list)):
        player_dict = player.model_dump()
        player_dict["id"] = give_id(player_list, "id")
        player_list.append(player_dict)
        write_entity(player_list, "Player")
        return player_dict
    else:
        raise HTTPException(status_code=400, detail="Player already exists")

@app.post("/add/club")
def add_club(club: Club):
    club_list = get_entities("Club")
    if (not redudancy_check(club.name, club_list)):
        club_dict = club.model_dump()
        club_dict["club_id"] = give_id(club_list, "club_id")
        club_list.append(club_dict)
        write_entity(club_list, "Club")
        return club_dict
    else:
        raise HTTPException(status_code=400, detail= "Club already exists")

def readData():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            content = json.load(file)
            return content
    except Exception as e:
        return { "Player": [], "Club": [] }

def writeData(data: list):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def write_entity(file: dict, key: str):
    current_list = readData()
    current_list[key] = file
    writeData(current_list)

def get_entities(key_name: str):
    return readData().get(key_name, [])
    

#helper functions

def give_id(lists: list, key: str):
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

def hasClub(id: int):
    clubs = get_entities("Club")
    club_ids = [c["club_id"] for c in clubs]
    if id in club_ids:
        return True
    return False
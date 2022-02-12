from pymongo import MongoClient
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from datetime import datetime

app = FastAPI()

client = MongoClient('mongodb://localhost', 27017)

db = client['miniproject']

class Room(BaseModel):
    Room: int
    Status: int
    Time: Optional[int] = None

col1 = db['Room']
col2 = db['estimate_1']
col3 = db['estimate_2']
col4 = db['estimate_3']


@app.post("/add/")
def add_time(r: Room):
    if r.Status == 0:
        r.Time = datetime.now().timestamp()
        query = {"Room": r.Room}
        new_value = {"$set": {"Time": r.Time}}
        col1.update_one(query, new_value)
        return {
            "result": "enter room {}".format(r.Room) 
        }

    elif r.Status == 1:
        query = {"Room": r.Room}
        time = col1.find_one(query, {"_id": 0,"Time": 1})
        res = datetime.now().timestamp() - time["Time"]
        if r.Room == 1:
            col2.insert_one({"Time": res})
        elif r.Room == 2:
            col3.insert_one({"Time": res})
        else:
            col4.insert_one({"Time": res})
        return {
            "result": "exit room {}".format(r.Room),
            "time use": res
        }

@app.get("/get/time_used/{room}")
def show_time_used(room: int):
    query = {"Room": room}
    time = col1.find_one(query, {"_id": 0,"Time": 1})
    res = datetime.now().timestamp() - time["Time"]
    res = datetime.fromtimestamp(res).strftime("%M:%S")
    return {
        "time used": res
    }


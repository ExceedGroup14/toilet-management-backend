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

    elif r.Status == 1:
        query = {"Room": r.Room}
        time = col1.find_one(query, {"_id": 0, "Time": 1})
        res = datetime.now().timestamp() - time["Time"]
        if r.Room == 1:
            col2.insert_one(res)
        elif r.Room == 2:
            col3.insert_one(res)
        else:
            col4.insert_one(res)


def calculate_estimatetime(db):
    all_time = db.find()
    list_time = []
    for i in all_time:
        list_time.append(i['Time'])
    result = sum(list_time) / len(list_time)
    result = datetime.fromtimestamp(result).strftime("%S")
    return result


@app.get("/show_estimate/{room}")
def get_estimate_time(room: int):
    if room == 1:
        result = calculate_estimatetime(col2)
        return {"Time": result}
    elif room == 2:
        result = calculate_estimatetime(col3)
        return {"Time": result}
    elif room == 3:
        result = calculate_estimatetime(col4)
        return {"Time": result}

from pymongo import MongoClient
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from datetime import datetime
import time

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
        new_value = {"$set": {"Time": r.Time, "Status": r.Status}}
        col1.update_one(query, new_value)
        return {
            "result": "enter room {}".format(r.Room) 
        }

    elif r.Status == 1:
        query = {"Room": r.Room}
        time = col1.find_one(query, {"_id": 0, "Time": 1})
        res = datetime.now().timestamp() - time["Time"]
        if r.Room == 1:
            col2.insert_one({"Time": res})
        elif r.Room == 2:
            col3.insert_one({"Time": res})
        else:
          col4.insert_one({"Time": res})
        new_value = {"$set": {"Time": None, "Status": r.Status}}
        col1.update_one(query, new_value)
        return {
            "result": "exit room {}".format(r.Room),
            "time use": res
        }
          
@app.get('/time/{r}')
def op(r:int):
    if r== 1:
        query= {"Room": r}
        result = col1.find({"Room":1},{"_id":0})
        result1 = list(result)
        result1[0]['Time'] = datetime.fromtimestamp(result1[0]['Time']).strftime("%H:%M")
        print(result1[0]['Time'])
        if len(result1)!=0:
         return result1[0]
    elif r== 2:
        query= {"Room": r}
        result = col1.find({"Room":2},{"_id":0})
        result1 = list(result)
        result1[0]['Time'] = datetime.fromtimestamp(result1[0]['Time']).strftime("%H:%M")
        if len(result1)!=0:
         return result1[0]
    elif r== 3:
        query= {"Room": r}
        result = col1.find({"Room":3},{"_id":0})
        result1 = list(result)
        result1[0]['Time'] = datetime.fromtimestamp(result1[0]['Time']).strftime("%H:%M")
        if len(result1)!=0:
         return result1[0] 

@app.get("/get/time_used/{room}")
def show_time_used(room: int):
    query = {"Room": room}
    time = col1.find_one(query, {"_id": 0,"Time": 1})
    res = datetime.now().timestamp() - time["Time"]
    res = datetime.fromtimestamp(res).strftime("%M:%S")
    return {
        "time used": res
    }

def calculate_estimatetime(db):
    all_time = db.find()
    list_time = []
    for i in all_time:
        list_time.append(i['Time'])
    result = sum(list_time) / len(list_time)
    result = datetime.fromtimestamp(result).strftime("%M:%S")
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

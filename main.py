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
        new_value = {"$set": {"Time": r.Time}}
        col1.update_one(query, new_value)

    elif r.Status == 1:
        query = {"Room": r.Room}
        time = col1.find_one(query, {"_id": 0,"Time": 1})
        res = datetime.now().timestamp() - time["Time"]
        if r.Room == 1:
            col2.insert_one(res)
        elif r.Room == 2:
            col3.insert_one(res)
        else:
            col4.insert_one(res)
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
from pymongo import MongoClient
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from datetime import datetime

app = FastAPI()

client = MongoClient('mongodb://localhost', 27017)

db = client['miniproject']


@app.get('/')
def get_time(time: datetime):
    print(time)
    return {"time": time}

from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum
from datetime import datetime
import uuid

app = FastAPI()

@app.get("/")
def read_root():
    return {"JUSTPAY"}








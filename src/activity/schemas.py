from pydantic import BaseModel
from datetime import datetime


class CollarActivity(BaseModel):
    collar: str
    x: float
    y: float
    z: float

class NewCollarActivity(BaseModel):
    collar_id: int
    x: float
    y: float
    z: float
    datetime: datetime

class FeederFeed(BaseModel):
    feeder: str

class NewFeederFeed(BaseModel):
    feeder_id: int
    datetime: datetime
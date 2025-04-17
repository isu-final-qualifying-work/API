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

class LitterClean(BaseModel):
    litter: str
    collar: str

class NewLitterClean(BaseModel):
    litter_id: int
    collar_id: int
    datetime: datetime

class Eating(BaseModel):
    feeder: str
    collar: str
    size: int

class NewEating(BaseModel):
    feeder_id: int
    collar_id: int
    size: int
    datetime: datetime
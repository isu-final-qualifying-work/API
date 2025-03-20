from pydantic import BaseModel
from src.auth.schemas import Token


class Feeder(BaseModel):
    id: int
    name: str

class NewFeeder(Token):
    name: str

class FeederID(BaseModel):
    id: int

class FullFeederData(BaseModel):
    id: int
    name: str
    collars: list
    schedule: list
    timezone: int
    size: int

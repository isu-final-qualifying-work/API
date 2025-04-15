from pydantic import BaseModel
from src.auth.schemas import Token


class Collar(BaseModel):
    id: int
    name: str

class NewCollar(Token):
    name: str
    device_id: int
    device_type: str
    pet_name: str
    gender: str
    kitten: bool
    pregnant: bool
    sterilized: bool
    weight: int

class CollarID(BaseModel):
    id: int

class CollarByFeeder(BaseModel):
    feeder_name: str

class CollarByLitter(BaseModel):
    litter_name: str
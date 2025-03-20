from pydantic import BaseModel
from src.auth.schemas import Token


class Litter(BaseModel):
    id: int
    name: str

class NewLitter(Token):
    name: str

class LitterID(BaseModel):
    id: int

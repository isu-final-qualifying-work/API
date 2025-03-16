from pydantic import BaseModel


class Litter(BaseModel):
    id: int
    name: str

class NewLitter(BaseModel):
    name: str
    user_id: int

class LitterID(BaseModel):
    id: int

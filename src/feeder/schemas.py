from pydantic import BaseModel


class Feeder(BaseModel):
    id: int
    name: str

class NewFeeder(BaseModel):
    name: str
    user_id: int

class FeederID(BaseModel):
    id: int

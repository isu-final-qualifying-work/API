from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    password: str

class NewUser(BaseModel):
    name: str
    password: str

class UserID(BaseModel):
    id: int



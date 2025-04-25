from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    email: str
    password: str

class NewUser(BaseModel):
    name: str
    email: str
    password: str

class LoginUser(BaseModel):
    email: str
    password: str

class UserID(BaseModel):
    id: int



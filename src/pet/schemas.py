from pydantic import BaseModel


class Pet(BaseModel):
    id: int
    name: str
    gender: str
    type: str
    is_child: bool
    weight: int
    is_pregnant: bool
    is_sterilized: bool
    collar_id: int


class NewPet(BaseModel):
    name: str
    gender: str
    type: str
    is_child: bool
    weight: int
    is_pregnant: bool
    is_sterilized: bool
    collar_id: int
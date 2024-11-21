from pydantic import BaseModel
from datetime import datetime


class CollarActivity(BaseModel):
    collar: str
    x: float
    y: float
    z: float

class NewCollarActivity(BaseModel):
    collar: str
    x: float
    y: float
    z: float
    datetime: datetime

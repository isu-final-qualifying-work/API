from pydantic import BaseModel
from datetime import datetime


class EatingActivityFilter(BaseModel):
    pet_id: int
    type: str
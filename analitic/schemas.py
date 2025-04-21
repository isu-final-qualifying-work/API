from pydantic import BaseModel
from datetime import datetime


class ActivityFilter(BaseModel):
    pet_id: int
    type: str
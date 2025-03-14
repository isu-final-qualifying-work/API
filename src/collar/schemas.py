from pydantic import BaseModel


class Collar(BaseModel):
    id: int
    name: str

class NewCollar(BaseModel):
    name: str
    device_id: int
    device_type: str

class CollarID(BaseModel):
    id: int

class CollarByFeeder(BaseModel):
    feeder_name: str

class CollarByLitter(BaseModel):
    litter_name: str
from pydantic import BaseModel


class Setting(BaseModel):
    id: int
    size: int
    #schedule: list

class NewSetting(BaseModel):
    size: int
    #schedule: list
    feeder_id: int

class SettingID(BaseModel):
    id: int

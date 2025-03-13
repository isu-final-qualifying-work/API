from pydantic import BaseModel


class Setting(BaseModel):
    id: int
    size: int
    schedule: list[list]
    timezone: int

class NewSetting(BaseModel):
    size: int
    schedule: list[list]
    feeder_id: int
    timezone: int

class SettingID(BaseModel):
    id: int

class SettingByFeeder(BaseModel):
    feeder_name: str
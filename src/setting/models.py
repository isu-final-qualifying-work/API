from sqlalchemy import Column, Integer, ForeignKey, ARRAY
from src.database import Base
from sqlalchemy.orm import relationship

class Feeder_Settings(Base):
    __tablename__ = 'feeder_settings'
    id = Column(Integer, primary_key=True)
    feeder_id =  Column(Integer, ForeignKey("feeders.id"))
    setting_id =  Column(Integer, ForeignKey("settings.id"))

class Settings(Base):
    __tablename__ = 'settings'
    id = Column(Integer, primary_key=True)
    size = Column(Integer, nullable=False, autoincrement=30)
    #schedule = Column(ARRAY(Integer), nullable=False)
    feeders = relationship("Feeder_Settings", backref="setting")
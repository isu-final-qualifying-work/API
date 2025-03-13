from sqlalchemy import Column, Integer, ForeignKey, ARRAY
from src.database import Base
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship

class Feeder_Settings(Base):
    __tablename__ = 'feeder_settings'
    id = Column(Integer, primary_key=True)
    feeder_id =  Column(Integer, ForeignKey("feeders.id"))
    setting_id =  Column(Integer, ForeignKey("settings.id"))

class Settings(Base):
    __tablename__ = 'settings'
    id = Column(Integer, primary_key=True)
    size = Column(Integer, nullable=False, default=30)
    schedule = Column(postgresql.ARRAY(Integer, dimensions=2), nullable=False, default=[[8, 0]])
    timezone = Column(Integer, nullable=False, default=0)
    feeders = relationship("Feeder_Settings", backref="setting")
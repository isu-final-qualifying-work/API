from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from src.database import Base
from sqlalchemy.orm import relationship

class User_Feeder(Base):
    __tablename__ = 'user_feeder'
    id = Column(Integer, primary_key=True)
    user_id =  Column(Integer, ForeignKey("users.id"))
    feeder_id =  Column(Integer, ForeignKey("feeders.id"))

class Feeders(Base):
    __tablename__ = 'feeders'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)    
    users = relationship("User_Feeder", backref="feeder")
    collars = relationship("Feeder_Collar", backref="feeder")
    setting = relationship("Settings", back_populates="feeder")
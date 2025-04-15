from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from src.database import Base
from sqlalchemy.orm import relationship

class Feeder_Collar(Base):
    __tablename__ = 'feeder_collar'
    id = Column(Integer, primary_key=True)
    collar_id =  Column(Integer, ForeignKey("collars.id"))
    feeder_id =  Column(Integer, ForeignKey("feeders.id"))

class Litter_Collar(Base):
    __tablename__ = 'litter_collar'
    id = Column(Integer, primary_key=True)
    collar_id =  Column(Integer, ForeignKey("collars.id"))
    litter_id =  Column(Integer, ForeignKey("litters.id"))

class Collars(Base):
    __tablename__ = 'collars'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)    
    feeders = relationship("Feeder_Collar", backref="collar")
    litters = relationship("Litter_Collar", backref="collar")
    pet = relationship("Pets", back_populates="collar")
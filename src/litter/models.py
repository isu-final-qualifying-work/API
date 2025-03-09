from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from src.database import Base
from sqlalchemy.orm import relationship

class User_Litter(Base):
    __tablename__ = 'user_litter'
    id = Column(Integer, primary_key=True)
    user_id =  Column(Integer, ForeignKey("users.id"))
    litter_id =  Column(Integer, ForeignKey("litters.id"))

class Litters(Base):
    __tablename__ = 'litters'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)    
    users = relationship("User_Litter", backref="litter")
    collars = relationship("Litter_Collar", backref="litter")
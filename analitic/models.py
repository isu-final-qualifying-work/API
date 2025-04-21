from sqlalchemy import Column, Integer, String, Boolean, Numeric
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ActivityReference(Base):
    __tablename__ = "activity_reference"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(10))              
    is_child = Column(Boolean)             
    gender = Column(String(1))             
    is_sterilized = Column(Boolean)
    is_pregnant = Column(Boolean)
    min = Column(Integer)                 
    max = Column(Integer)                  


class LitterReference(Base):
    __tablename__ = "litter_reference"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(10))
    is_child = Column(Boolean)
    gender = Column(String(1))
    is_sterilized = Column(Boolean)
    is_pregnant = Column(Boolean)
    min = Column(Integer)                  
    max = Column(Integer)                 


class EatingKoef(Base):
    __tablename__ = "eating_koef"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(10))              
    category = Column(String(10))          
    min = Column(Numeric(4, 1))            
    max = Column(Numeric(4, 1))            

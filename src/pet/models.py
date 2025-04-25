from sqlalchemy import Column, Integer, ForeignKey, Boolean, String, CHAR
from src.database import Base
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship

class Pets(Base):
    __tablename__ = 'pets'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    gender = Column(CHAR, nullable=False)
    type = Column(String, nullable=False)
    is_child = Column(Boolean, nullable=False)
    weight = Column(Integer, default=None)
    is_pregnant = Column(Boolean, nullable=False, default=False)
    is_sterilized = Column(Boolean, nullable=False, default=False)
    collar_id = Column(Integer, ForeignKey('collars.id'))
    collar = relationship('Collars', back_populates='pet')
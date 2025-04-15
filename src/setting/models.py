from sqlalchemy import Column, Integer, ForeignKey, ARRAY
from src.database import Base
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship

class Settings(Base):
    __tablename__ = 'settings'
    id = Column(Integer, primary_key=True)
    size = Column(Integer, nullable=False, default=30)
    schedule = Column(postgresql.ARRAY(Integer, dimensions=2), nullable=False, default=[[8, 0]])
    timezone = Column(Integer, nullable=False, default=0)
    feeder_id = Column(Integer, ForeignKey('feeders.id'))
    feeder = relationship('Feeders', back_populates='setting')
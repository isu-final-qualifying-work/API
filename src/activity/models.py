from sqlalchemy import Column, Integer, String, Float, DateTime
from src.database import Base


class CollarsActivity(Base):
    __tablename__ = "collars_activity"

    id = Column(Integer, primary_key=True, index=True)
    #collar_id = Column(Integer)
    collar = Column(String)
    x = Column(Float)
    y = Column(Float)
    z = Column(Float)
    datetime = Column(DateTime)
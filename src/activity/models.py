from sqlalchemy import Column, Integer, String, Float, DateTime
from src.database import Base


class CollarsActivity(Base):
    __tablename__ = "collars_activity"

    id = Column(Integer, primary_key=True, index=True)
    collar_id = Column(Integer)
    #collar = Column(String)
    # x = Column(Float)
    # y = Column(Float)
    # z = Column(Float)
    datetime = Column(DateTime)


class FeederFeeds(Base):
    __tablename__ = "feeder_feeds"

    id = Column(Integer, primary_key=True, index=True)
    feeder_id = Column(Integer)
    datetime = Column(DateTime)


class LitterCleans(Base):
    __tablename__ = "litter_cleans"

    id = Column(Integer, primary_key=True, index=True)
    litter_id = Column(Integer)
    collar_id = Column(Integer)
    datetime = Column(DateTime)

class EatingActivity(Base):
    __tablename__ = "eating_activity"

    id = Column(Integer, primary_key=True, index=True)
    feeder_id = Column(Integer)
    collar_id = Column(Integer)
    size = Column(Float)
    datetime = Column(DateTime)
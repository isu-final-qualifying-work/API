from sqlalchemy import Column, Integer, String
from src.database import Base
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    feeders = relationship("User_Feeder", backref='user')
    litters = relationship("User_Litter", backref='user')

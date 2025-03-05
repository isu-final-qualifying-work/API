from sqlalchemy import Column, Integer, String, Float, DateTime
from src.database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    password = Column(String)

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.config.env import DICT_ENVS

BASE_IP = DICT_ENVS['BASE_IP']
BASE_PORT = DICT_ENVS['BASE_PORT']
USER_NAME = DICT_ENVS['USER_NAME']
USER_PASS = DICT_ENVS['USER_PASS']
DB_NAME = DICT_ENVS['DB_NAME']


DB_URL = f"postgresql://{USER_NAME}:{USER_PASS}@{BASE_IP}:{BASE_PORT}/{DB_NAME}"

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
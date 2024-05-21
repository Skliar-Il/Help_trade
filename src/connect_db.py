from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy import create_engine
from typing import AsyncGenerator
import os
import sys

from config import POSTGRES_HOST, POSTGRES_NAME, POSTGRES_PASSWORD, POSTGRES_USER, POSTGRES_PORT


class Base(DeclarativeBase):
    pass

DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_NAME}"

engine = create_engine(DATABASE_URL)

session_maker = sessionmaker(engine, expire_on_commit=False)



        

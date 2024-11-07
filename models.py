from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import URL
import os

## url for db from config
DB_URL = URL.create(
    drivername = "postgresql+psycopg2",
    username   = os.environ["PGSQL_USER"],
    password   = os.environ["PGSQL_PASS"],
    host       = os.environ["PGSQL_HOST"],
    database   = os.environ["PGSQL_DB"]
)

## engine creation for db connection
engine = create_engine(DB_URL, echo=True)

## Base class and models declarations
Base = declarative_base()

class User(Base):
    __tablename__  = "Users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    role = Column(Integer)


class Role(Base):
    __tablename__ = "Roles"
    id = Column(Integer, primary_key=True)
    name = Column(String)

Base.metadata.create_all(engine)



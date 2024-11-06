from app.db.db import engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text

"""
<app/db/models.py>

This is where you place models (tables) for the database.

"""

Base = declarative_base()

class Todo(Base):
    __tablename__ = "Todo"

    id = Column(Integer, primary_key=True)
    text = Column(String)
    is_done = Column(Boolean, default=False)

class Events(Base):
    __tablename__ = "Events"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    photo = Column(String)
    location = Column(String)
    description = Column(String)
    type = Column(String)
    start_at = Column(DateTime)
    end_at = Column(DateTime)
    group_name = Column(String)

class Messages(Base):
    __tablename__ = "Messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    subject = Column(String)
    message = Column(Text)
    role = Column(Integer)
    date = Column(DateTime)

Base.metadata.create_all(engine)
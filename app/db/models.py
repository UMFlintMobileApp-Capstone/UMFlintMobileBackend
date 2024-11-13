from app.db.db import engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, UUID

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
    description = Column(Text)
    type = Column(String)
    start_at = Column(DateTime)
    end_at = Column(DateTime)
    group_name = Column(String)
    url = Column(String)

class Announcements(Base):
    __tablename__ = "Announcements"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    description = Column(Text)
    role = Column(String)
    dateStart = Column(DateTime)
    dateEnd = Column(DateTime)

class Maps(Base):
    __tablename__ = "Maps"

    id = Column(Integer, primary_key=True)
    building_name = Column(String)
    floor_num = Column(Integer)
    map_img = Column(String)

class BuildingHours(Base):
    __tablename__ = "Building Hours"

    building = Column(String, primary_key=True)
    open_at = Column(DateTime)
    close_at = Column(DateTime)

class User(Base):
    __tablename__  = "Users"

    id = Column(Integer, primary_key=True)
    email = Column(String)
    firstname = Column(String)
    surname = Column(String)
    role = Column(Integer)
    profilePicture = Column(String)


class Role(Base):
    __tablename__ = "Roles"

    id = Column(Integer, primary_key=True)
    name = Column(String)

class News(Base):
    __tablename__ = "News"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    url = Column(String)
    publication_date = Column(DateTime)
    excerpt = Column(String)
    image_url = Column(String)
    author_name = Column(String)
    author_email = Column(String)

class Messages(Base):
    __tablename__ = "Messages"

    id = Column(Integer, primary_key=True)
    user = Column(Integer)
    messageUuid = Column(UUID)
    chatUuid = Column(UUID)
    message = Column(Text)
    sendDate = Column(DateTime)

class Threads(Base):
    __tablename__ = "Threads"

    uuid = Column(UUID, primary_key=True)
    user = Column(Integer, primary_key=True)

Base.metadata.create_all(engine)
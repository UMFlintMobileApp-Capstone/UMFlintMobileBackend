from app.db.db import engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean

Base = declarative_base()

class Todo(Base):
    __tablename__ = "Todo"

    id = Column(Integer, primary_key=True)
    text = Column(String)
    is_done = Column(Boolean, default=False)

Base.metadata.create_all(engine)
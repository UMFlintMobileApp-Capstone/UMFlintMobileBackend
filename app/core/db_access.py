from app.db.db import session
from app.db.models import News, Announcements, Maps, BuildingHours, User, Blocks
import sys

print(sys.path)
##from app.db.models import News

def get_news():
    return session.query(News).all()

def get_announcements():
    return session.query(Announcements).all()

def get_maps():
    return session.query(Maps).all()

def get_hours():
    return session.query(BuildingHours).all()

def getUserByEmail(email: str):
    return session.query(User).filter(User.email==email).first()

def getUserById(id: int):
    return session.query(User).filter(User.id==id).first()

def getUsers():
    return session.query(User).all()
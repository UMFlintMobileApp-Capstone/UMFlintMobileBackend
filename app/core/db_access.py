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
    user = session.query(User).filter(User.email==email)
    if user.count() != 0:
        return user.first()
    else:
        return {
            "email": email,
            "firstname": "",
            "role": 0,
            "id": -1,
            "surname": "",
            "profilePicture": ""
            }

def getUserById(id: int):
    user = session.query(User).filter(User.id==id)
    if user.count() != 0:
        return user.first()
    else:
        return {
            "email": "",
            "firstname": "",
            "role": 0,
            "id": id,
            "surname": "",
            "profilePicture": ""
            }


def getUsers():
    return session.query(User).all()
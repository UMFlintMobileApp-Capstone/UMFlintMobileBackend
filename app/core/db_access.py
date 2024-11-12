from app.db.db import session
from app.db.models import News, Announcements
import sys

print(sys.path)
##from app.db.models import News

def get_news():
    return session.query(News).all()

def get_announcements():
    return session.query(Announcements).all()

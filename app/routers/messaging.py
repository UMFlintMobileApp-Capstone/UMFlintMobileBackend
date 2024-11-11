from fastapi import APIRouter
from app.core.umich_api import get_announcement_items
from app.db.db import session
from app.db.models import Announcements
from datetime import datetime

""" 
<app/routers/messaging.py>

"""

# create the router
router = APIRouter()

@router.get("/announcements/get/{items}")
def getMessages(items):
    index = 0

    allAnnouncements=[]
    for announcement in get_announcement_items()['data']:
        if announcement['display_start']!="":
            dateStart = announcement['display_start']
        else:
            dateStart = announcement['published_at']

        roles = []
        for role in announcement['affiliations']:
            roles.append({'role': getRoleId(role['name'])})

        announcementJson = {
                    'id': announcement['id'],
                    'title': announcement['title'],
                    'description':announcement['description'],
                    'dateStart': dateStart,
                    'dateEnd': announcement['display_end'],
                    'roles': roles
                }

        allAnnouncements.append(announcementJson)
        index = index+1

    for announcement in session.query(Announcements).all():
        roles = []
        for role in announcement.role.split(","):
            roles.append({'role': role})

        announcementJson = {
                    'id': announcement.id,
                    'title': announcement.title,
                    'description':announcement.description,
                    'dateStart': announcement.dateStart,
                    'dateEnd': announcement.dateEnd,
                    'roles': roles
                }

        allAnnouncements.append(announcementJson)

    allAnnouncements.sort(key=lambda d: datetime.strptime(d['dateStart'], "%Y-%m-%d %H:%M:%S"), reverse=True)

    if(items.isnumeric()):
        return allAnnouncements[:int(items)]
    else:
        return allAnnouncements


def getRoleId(name):
    if name=="student":
        return 1
    elif name=="staff":
        return 2
    elif name=="faculty":
        return 3
    else:
        return 0
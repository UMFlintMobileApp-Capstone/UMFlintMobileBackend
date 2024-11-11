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
    # create a list of all announcements
    allAnnouncements=[]

    # get from the umflint api, iterate for each
    for announcement in get_announcement_items()['data']:
        # some clean up for getting the start date (some only have publish at)
        if announcement['display_start']!="":
            dateStart = announcement['display_start']
        else:
            dateStart = announcement['published_at']

        # get all the roles
        roles = []
        for role in announcement['affiliations']:
            roles.append({'role': getRoleId(role['name'])})

        # create a dictionary of an individual announcement
        announcementJson = {
                    'id': announcement['id'],
                    'title': announcement['title'],
                    'description':announcement['description'],
                    'dateStart': dateStart,
                    'dateEnd': announcement['display_end'],
                    'roles': roles
                }

        # add the dictionary to the list
        allAnnouncements.append(announcementJson)

    # get from the database, iterate for each
    for announcement in session.query(Announcements).all():
        # get all the roles (and since it's comma seperated, iterate)
        roles = []
        for role in announcement.role.split(","):
            roles.append({'role': role})

        # create a dictionary of an individual announcement
        announcementJson = {
                    'id': announcement.id,
                    'title': announcement.title,
                    'description':announcement.description,
                    'dateStart': announcement.dateStart,
                    'dateEnd': announcement.dateEnd,
                    'roles': roles
                }

        # add the dictionary to the list
        allAnnouncements.append(announcementJson)

    # sort by newest start date
    allAnnouncements.sort(key=lambda d: datetime.strptime(d['dateStart'], "%Y-%m-%d %H:%M:%S"), reverse=True)

    # if the query is a number, return by a max number of items, otherwise all
    if(items.isnumeric()):
        return allAnnouncements[:int(items)]
    else:
        return allAnnouncements

# based on the name, give a role id to match database
def getRoleId(name):
    if name=="student":
        return 1
    elif name=="staff":
        return 2
    elif name=="faculty":
        return 3
    else:
        return 0
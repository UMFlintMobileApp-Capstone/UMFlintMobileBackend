from fastapi import APIRouter
import requests

""" 
<app/routers/messaging.py>

"""

# create the router
router = APIRouter()

@router.get("/messages/")
def getMessages():
    index = 0
    announcements = requests.get('https://www.umflint.edu/wp-json/wp-content-types/announcements').json()

    allAnnouncements=[]
    for announcement in announcements['data']:
        id = announcement['id']
        title = announcement['title']
        description = announcement['description']

        if announcement['display_start']!="":
            dateStart = announcement['display_start']
        else:
            dateStart = announcement['published_at']

        dateEnd = announcement['display_end']

        roles = []
        for role in announcement['affiliations']:
            roles.append({'role':getRoleId(role['name'])})

        announcementJson= {
                    'id': id,
                    'title': title,
                    'description':description,
                    'dateStart': dateStart,
                    'dateEnd': dateEnd,
                    'roles': roles
                }
        
        allAnnouncements.append(announcementJson)
        index = index+1

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
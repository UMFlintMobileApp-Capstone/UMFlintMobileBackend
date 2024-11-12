from fastapi import APIRouter,Depends
from app.db.db import session
from app.db.models import Todo
from app.core.auth import get_logged_user
from fastapi_sso.sso.base import OpenID
from app.core.umich_api import get_events_groups, get_events_items

""" 
<app/routers/events.py>

"""

router = APIRouter()
#Grab all events from the umflint API
@router.get("/events/get/{items}")
async def getEvents(items):
    
    #get all group slugs first
    all_events = []

    for slug in get_events_groups()['data']:
        
        #loop through each slug to get all events into an array
        for event in get_events_items(slug['slug']):
            events_json = {
                'id' : event['id'],
                'title' : event['title'],
                'description' : event['description'],
                'url' : event['url'],
                'start_at' : event['start_at'],
                'end_at' : event['end_at'],
                'photo' : event['photo'],
                'location' : event['location'],
                'type' : event['type'],
            }

            all_events.append(events_json)
    
    #sort array by unix Epoch
    all_events.sort(key = lambda start: start['start_at'], reverse=True)
    
    #grab top most events
    if(items.isnumeric()):
        return all_events[:int(items)]
    else:
        return all_events

from fastapi import APIRouter
from app.core.umich_api import get_events_groups, get_events_items

""" 
<app/routers/events.py>

"""

router = APIRouter()
#Grab all events from the umflint API
@router.get("/events/get/{items}")
async def get_events(items):
    
    #initialize arrays for gathering events from API
    all_events = []
    unique_events = []

    #get all group slugs first
    for slug in get_events_groups()['data']:
        
        #loop through each slug to get all events into an array
        for event in get_events_items(slug['slug'])['data']:
            events_json = {
                'id' : event['id'],
                'title' : event['title'],
                'description' : event['description'],
                'url' : event['url'],
                'start_at' : event['start_at'],
                'end_at' : event['end_at'],
                'photo' : event['photo'],
                'location_type' : event['location_type'],
                'type' : event['type'],
            }

            #If there is an event with the same title, don't add
            if(event['title'] not in unique_events):
                all_events.append(events_json)
                unique_events.append(event['title'])
    
    #sort array by unix Epoch
    all_events.sort(key = lambda start: start['start_at'], reverse=True)
    
    #grab top most events
    if(items.isnumeric()):
        return all_events[:int(items)]
    else:
        return all_events

#get_events(3)
from fastapi import APIRouter
from app.core.data_process import get_announcement_items
""" 
<app/routers/messaging.py>

"""

# create the router
router = APIRouter()

# retrieve announcements from db and api
@router.get("/announcements/get/{items}")
def getMessages(items):
    return get_announcement_items(items)
    
    


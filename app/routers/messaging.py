from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.umich_api import get_announcement_items
from app.db.db import session
from app.db.models import Messages
from app.core.connectionmanager import ConnectionManager
from datetime import datetime
from app.core.auth import getUserDetails

from fastapi import APIRouter
from app.core.data_process import get_announcement_items
""" 
<app/routers/messaging.py>

"""

# create the router
router = APIRouter()
manager = ConnectionManager()

# retrieve announcements from db and api
@router.get("/announcements/get/{items}")
def getMessages(items):
    return get_announcement_items(items)
    
    

@router.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket, token: str):
    client_id = getUserDetails(token)

    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_json()

            message = {
                'type': 'personal',
                'text': data['text'],
                'to': data['to'],
                'id': data['id'],
                'date': data['date']
            }

            session.add(Messages(
                sendUser=data['id'],
                sentUsers=data['to'],
                text=data['text'],
                sendDate=datetime.strftime('%Y-%m-%d %H:%M:%S', data['date'])
            ))
            session.commit()

            await manager.pm(message, websocket)

            message['type']='dm'

            await manager.dm(message)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

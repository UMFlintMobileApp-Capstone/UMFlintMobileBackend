from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from app.core.umich_api import get_announcement_items
from app.db.db import session
from app.db.models import Messages, Threads
from app.core.connectionmanager import ConnectionManager
from app.core.auth import getUserDetails
from sqlalchemy import desc
import uuid

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

    await manager.connect(websocket, client_id.id)
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

            createThread = False

            for x in data['to']:
                if session.query(Threads.uuid).filter(Threads.user==x).count() == 0:
                    createThread = True
                    break

            if createThread:
                tId = uuid.uuid4()

                session.add(
                    Threads(
                        uuid = tId,
                        user = client_id.id
                    )
                )

                for x in data['to']:
                    session.add(
                        Threads(
                            uuid = tId,
                            user = x
                        )
                    )
            else:
                tId = session.query(Threads.uuid).filter(Threads.user==x).first().uuid

            session.add(
                Messages(
                    user=client_id.id,
                    messageUuid=uuid.uuid4(),
                    chatUuid=tId,
                    message=data['text'],
                    sendDate=data['date']
                )
            )         

            session.commit()

            await manager.pm(message, websocket)

            message['type']='dm'

            await manager.dm(message)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@router.get("/messages/")
async def getChats(token: str):
    user = getUserDetails(token)

    threads = []

    for thread in session.query(Threads).filter(Threads.user==user.id).all():
        users = []

        for u in session.query(Threads).filter(Threads.uuid==thread.uuid).all():
            users.append({"id": u.user})

        lastMessage = session.query(Messages).filter(
                Messages.chatUuid==thread.uuid
            ).order_by(
                desc(Messages.sendDate)
            ).first()

        threads.append({
            "uuid": thread.uuid,
            "users": users,
            "last_message": 
                {
                "messageUuid": lastMessage.messageUuid,
                "message": lastMessage.message,
                "sendDate": lastMessage.sendDate,
                "sender": lastMessage.user
                }
            }
        )

    return {'threads': threads}

@router.get("/messages/chat")
async def getChatMessages(token: str, id: str):
    user = getUserDetails(token)

    if session.query(Threads).filter(Threads.uuid==id, Threads.user==user.id).count() != 0:
        messages = []

        for message in session.query(Messages).filter(Messages.chatUuid==id).all():
            messages.append({
                "messageUuid": message.messageUuid,
                "threadUuid": message.chatUuid,
                "message": message.message,
                "sendDate": message.sendDate,
                "sender": message.user
            })

        return messages

@router.get("/messages/test")
def a():
    return HTMLResponse("""
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <label>To: </label><input type="text" id="to" autocomplete="off"/>
            <label>Message: </label><input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = "debug"
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/ws/?token=`+client_id);
            ws.onmessage = function(event) {
                data = JSON.parse(event.data)
                console.log(data);

                if(data.type==="personal"){
                    var messages = document.getElementById('messages')
                    var message = document.createElement('li')
                    var content = document.createTextNode("You wrote "+data.text+" to user "+data.to)
                    message.appendChild(content)
                    messages.appendChild(message)
                }else if(data.type==="dm"){
                    var messages = document.getElementById('messages')
                    var message = document.createElement('li')
                    var content = document.createTextNode("User "+data.id+" wrote: "+data.text)
                    message.appendChild(content)
                    messages.appendChild(message)
                }


            };
            function sendMessage(event) {
                const msg = {
                    type: "message",
                    to: [document.getElementById('to').value,2],
                    text: document.getElementById('messageText').value,
                    id: client_id,
                    date: new Date(Date.now()).toLocaleString(),
                };
                ws.send(JSON.stringify(msg));

                event.preventDefault()
            }
        </script>
    </body>
</html>
""")
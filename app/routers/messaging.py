from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from fastapi.responses import HTMLResponse
from app.core.umich_api import get_announcement_items
from app.db.db import session
from app.db.models import Messages, Threads, User
from app.core.connectionmanager import ConnectionManager
from app.core.auth import getUserDetails
from sqlalchemy import desc
import uuid

from fastapi import APIRouter
from app.core.data_process import get_announcement_items
""" 
<app/routers/messaging.py>

This is the announcements and messaging route. 

It handles getting and setting system wide announcements.

It also handles the messaging functionality, both real-time
and historical.

"""

# create the router
router = APIRouter()
manager = ConnectionManager()

# retrieve announcements from db and api
@router.get("/announcements/get/{items}")
def getAnnouncements(items):
    return get_announcement_items(items)

# web socket for real time messaging (adds to db too!)
@router.websocket("/messaging/ws/")
async def websocketEndpoint(websocket: WebSocket, user: User = Depends(getUserDetails)):
    # connect to the websocket with the client's id
    await manager.connect(websocket, user.id)
    try:
        # continuously watch for messages while socket is open
        while True:
            # get the json message the client sent
            data = await websocket.receive_json()

            # formulate the response message
            message = {
                'type': 'personal',
                'text': data['text'],
                'to': data['to'],
                'id': data['id'],
                'date': data['date']
            }

            # do we want to create a thread? default is no
            createThread = False

            # for every recipient
            for x in data['to']:
                # if there's no active thread with this recipent, then we need to create a new one
                if session.query(Threads.uuid).filter(Threads.user==x).count() == 0:
                    createThread = True
                    break
            
            # when we need to create a thread
            if createThread:
                # generate the thread uuid
                tId = uuid.uuid4()

                # create and add to session the new thread for the sender
                session.add(
                    Threads(
                        uuid = tId,
                        user = user.id
                    )
                )

                # for each recipient
                for x in data['to']:
                    # create and add to session new thread for the recipient
                    session.add(
                        Threads(
                            uuid = tId,
                            user = x
                        )
                    )
            # if we don't need to create a thread, we do need the existing thread uuid        
            else:
                tId = session.query(Threads.uuid).filter(Threads.user==x).first().uuid

            # create and add to session the message, link to the thread
            session.add(
                Messages(
                    user=user.id,
                    messageUuid=uuid.uuid4(),
                    chatUuid=tId,
                    message=data['text'],
                    sendDate=data['date']
                )
            )         

            # send to database
            session.commit()

            # send a personal message to the sender saying we got it (we don't have to show this, but it's good to get an ack)
            await manager.pm(message, websocket)

            # change the message type to a direct message
            message['type']='dm'

            # and send the message to any active client that should get it
            await manager.dm(message)
    except WebSocketDisconnect:
        # disconnect the socket when a user leaves, we can also send a message to other users if we wanted
        manager.disconnect(websocket)

# get all threads for the current user, the users involved, and the most recent message
@router.get("/messages/")
async def getThreads(user: User = Depends(getUserDetails)):
    threads = []

    # get all threads for the current user
    for thread in session.query(Threads).filter(Threads.user==user.id).all():
        users = []

        # get all users for a given thread
        for u in session.query(Threads).filter(Threads.uuid==thread.uuid).all():
            users.append({"id": u.user})
        
        # get the most recent message
        lastMessage = session.query(Messages).filter(
                Messages.chatUuid==thread.uuid
            ).order_by(
                desc(Messages.sendDate)
            ).first()

        # form dict and add to list
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
    
    # return all threads
    return {"threads": threads}

# get a thread's messages given it's uuid
@router.get("/messages/chat/{id}")
async def getMessages(token: str, id: str):
    # login our user
    user = getUserDetails(token)

    # if the thread exists and the user has access to it
    if session.query(Threads).filter(Threads.uuid==id, Threads.user==user.id).count() != 0:
        messages = []

        # get all messages in thread and add to a list of dicts
        for message in session.query(Messages).filter(Messages.chatUuid==id).all():
            messages.append({
                "messageUuid": message.messageUuid,
                "threadUuid": message.chatUuid,
                "message": message.message,
                "sendDate": message.sendDate,
                "sender": message.user
            })

        # return all messages
        return {"messages": messages}

# add a user to a given thread
@router.post("/messages/user")
async def addUserToThread(newUser: int, threadUuid: str, user: User = Depends(getUserDetails)):
    # get the thread if the user is a part of it
    thread = session.query(Threads).filter(Threads.user==user.id, Threads.uuid==threadUuid)

    # if there's any threads
    if thread.count() > 0:
        # add the requested user
        session.add(
            Threads(
                uuid = threadUuid,
                user = newUser
            )
        )
        session.commit()

        return {"status": "success", "message": "Sucessfully added user '"+str(newUser)+"' to thread '"+threadUuid+"'!"}
    else:
        return {"status": "failure", "message": "Couldn't modify '"+threadUuid+"' because either you do not own it, or it doesn't exist."}

# delete a user from a given thread
@router.delete("/message/user/{id}")
async def removeUserFromThread(deleteUser: int, threadUuid: str, user: User = Depends(getUserDetails)):
    # get the thread if the user is a part of it
    thread = session.query(Threads).filter(Threads.user==user.id, Threads.uuid==threadUuid)

    # if there's any threads
    if thread.count() > 0:
        # get the thread if the deletee is a part of it
        toBeDeletedUser = session.query(Threads).filter(Threads.user==deleteUser, Threads.uuid==threadUuid)

        # delete the user if they are a part of the thread
        if toBeDeletedUser.one_or_none != None:
            session.delete(
                Threads(
                    uuid = threadUuid,
                    user = deleteUser
                )
            )
            session.commit()
            return {"status": "success", "message": "Sucessfully deleted user '"+str(deleteUser)+"' from thread '"+threadUuid+"'!"}
        
    return {"status": "failure", "message": "Couldn't modify '"+threadUuid+"' because either you do not own it, or it doesn't exist."}

# delete a message for everyone given it's uuid
@router.delete("/messages/message/{id}")
async def deleteMessage(id: str, user: User = Depends(getUserDetails)):
    # get the given message specifically that the user sent themselves
    message = session.query(Messages).filter(Messages.user==user.id, Messages.messageUuid==id)

    # if they have sent the message
    if message.one_or_none != None:
        # delete it
        session.delete(message)
        session.commit()
        return {"status": "success", "message": "Sucessfully deleted message '"+id+"'!"}
    # otherwise they don't have the correct permissions, or the message doesn't exist
    else:
        return {"status": "failure", "message": "Couldn't delete '"+id+"' because either you do not own it, or it doesn't exist."}

# delete a thread for a given user given the thread uuid
@router.delete("/messages/thread/{id}")
async def deleteThread(id: str, user: User = Depends(getUserDetails)):
    # get the given thread specifically that the user has access to
    thread = session.query(Threads).filter(Threads.user==user.id, Threads.uuid==id)

    # if there's still a thread
    if thread.count() > 0:
        # if there's only the current user, then we can just delete all the messages
        if thread.count() == 1:
            messages = session.query(Messages).filter(Messages.chatUuid==id)
            session.delete(messages)

        # delete the thread
        session.delete(thread)
        session.commit()

        return {"status": "success", "message": "Sucessfully deleted thread '"+id+"'!"}
    
    return {"status": "failure", "message": "Couldn't delete '"+id+"' because either you do not own it, or it doesn't exist."}

@router.get("/messages/test")
def a(user: User = Depends(getUserDetails)):
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
            var client_id = """+user.id+"""
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/messaging/ws/?token=`+client_id);
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
                    to: [document.getElementById('to').value],
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
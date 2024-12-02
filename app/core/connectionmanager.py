from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections.append({'websocket':websocket, 'userid':client_id})

    def disconnect(self, websocket: WebSocket):
        for connection in self.active_connections:
            if connection['websocket']==websocket:
                self.active_connections.remove(connection)

    async def pm(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection['websocket'].send_json(message)
            
    async def dm(self, message: dict):
        for connection in self.active_connections:
            if connection['userid'] in message['to']:
                await connection['websocket'].send_json(message)
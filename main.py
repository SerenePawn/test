from email import message
from bottle_websocket import websocket
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import json


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

html = ""
with open('index.html') as f:
    html = f.read()

class ConnectionManager:
    def __init__(self):
        self.active_connections = []
        self.messages_count = {}
        # self.messages_count.setdefault

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.messages_count.update({id(websocket): 0})

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        self.messages_count.pop(id(websocket))

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    def get_val(self, websocket: WebSocket):
        self.messages_count[id(websocket)] += 1
        return self.messages_count.get(id(websocket))


manager = ConnectionManager()

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws/{client_id}")
async def my_ws(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            data = json.loads(data)['val']
            await manager.broadcast(f'{{"val":"<div>{manager.get_val(websocket)}. {data}</div>"}}')
    except WebSocketDisconnect:
        manager.disconnect(websocket)
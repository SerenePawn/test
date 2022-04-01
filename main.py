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

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws/")
async def my_ws(websocket: WebSocket):
    msg_numerate = 1
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            data = data['val']
            await websocket.send_json(
                {
                    "val":f"<div>{msg_numerate}. {data}</div>"
                }
            )
            msg_numerate += 1
    except WebSocketDisconnect:
        print('conn lost')

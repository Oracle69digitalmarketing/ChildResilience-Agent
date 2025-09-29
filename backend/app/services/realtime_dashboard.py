from fastapi import WebSocket
import json, asyncio

connected_clients = set()

async def connect_client(ws: WebSocket):
    await ws.accept()
    connected_clients.add(ws)

async def disconnect_client(ws: WebSocket):
    connected_clients.remove(ws)

async def broadcast_incident(incident: dict):
    if connected_clients:
        data = json.dumps(incident)
        await asyncio.gather(*(client.send_text(data) for client in connected_clients))

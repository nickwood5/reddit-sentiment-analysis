import asyncio
import websockets

async def hello():
    async with websockets.connect("ws://localhost:8000/444") as websocket:
        await websocket.send("Hello world!")
        await websocket.recv()

asyncio.run(hello())
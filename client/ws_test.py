import asyncio
import websockets, json
from flask import jsonify

async def hello():
    async with websockets.connect("ws://localhost:8001/d81229d9-981e-4c3d-9fe2-bac3b1afbf1a", ping_interval=None) as websocket:
        await websocket.send(json.dumps({"subreddit": "bitcoin", "after": 1662521042, "before": 1662607442}))
        while True:
            try:
                message = await websocket.recv()
                message = json.loads(message)
                print("Received message {} from server".format(message))
            except websockets.exceptions.ConnectionClosed:
                print("Client disconnected.  Do cleanup")
                break   


asyncio.run(hello())

#1662521042, 1662607442
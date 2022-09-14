import asyncio
import websockets, json
from flask import jsonify

async def hello():
    async with websockets.connect("ws://localhost:8000/444") as websocket:
        await websocket.send(json.dumps({"subreddit": "bitcoin", "after": 1662521042, "before": 1662607442}))
        await websocket.recv()

asyncio.run(hello())

#1662521042, 1662607442
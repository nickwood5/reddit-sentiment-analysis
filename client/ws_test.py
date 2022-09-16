import asyncio
import websockets, json
from flask import jsonify


local_host = True
if local_host:
    app_url = "ws://localhost:8003/BIG"
else:
    app_url = "wss://nickwood-reddit-sentiment.herokuapp.com/444"

async def hello():
    async with websockets.connect(app_url) as websocket:
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
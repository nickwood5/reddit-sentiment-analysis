import json, websockets, os, asyncio, threading

async def input_handler(websocket, client):
    global connected_users, player_speeds

    async for message in websocket:
        message = json.loads(message)
        #print("Received message {} from {}".format(message, client))

local_host = True

async def main():
    # Set the stop condition when receiving SIGTERM.

    if local_host:
        selected_host = "localhost"
        selected_port = "8000"
    else:
        selected_host = ""
        selected_port = os.environ["PORT"]

    async with websockets.serve(
        input_handler,
        host=selected_host,
        port=selected_port
    ):
        await asyncio.Future()


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

loop.run_until_complete(main())

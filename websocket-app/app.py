from asyncio.base_subprocess import WriteSubprocessPipeProto
import json, websockets, os, asyncio, threading, reddit_api_test, heapq
import multiprocessing, time


def print_squares(subreddit, after, before, websocket):
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(reddit_api_test.get_post_list(subreddit, after, before, websocket))
    loop.close()
    

async def input_handler(websocket, client):
    global connected_users, player_speeds
    print("START SERVER")

    async for message in websocket:
        message = json.loads(message)
        print("Received message {} from {}".format(message, client))
        thread1 = threading.Thread(target=print_squares, 
                           args=(message["subreddit"], message["after"], message["before"], websocket))
        thread1.start()
        
        

local_host = True

async def main():
    # Set the stop condition when receiving SIGTERM.

    if local_host:
        selected_host = "localhost"
        selected_port = "8003"
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


#!/usr/bin/env python

import asyncio
import websockets
import json

async def chat_client(name, server_ip, port = "8765"):
    async with websockets.connect(f"ws://{server_ip}:{port}") as websocket:
        print(f"Connected as {name}")

        async def send_messages():
            while True:
                msg = input("")
                if msg.lower() == "/quit":
                    print("Leaving chat...")
                    await websocket.close()
                    break
                await websocket.send(json.dumps({"name": name, "msg": msg}))


        async def receive_messages():
            async for message in websocket:
                data = json.loads(message)
                print(f"\r{data['name']}: {data['msg']}\nYou: ", end="")

        await asyncio.gather(send_messages(), receive_messages())

if __name__ == "__main__":
    name = input("Enter your name: ")
    server_ip = input("Enter server ip: ")
    asyncio.run(chat_client(name, server_ip))

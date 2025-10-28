#!/usr/bin/env python

import asyncio
import websockets
import json
import sys

async def async_input(prompt=""):
    """Non-blocking input using asyncio streams."""
    print(prompt, end="", flush=True)
    loop = asyncio.get_event_loop()
    reader = asyncio.StreamReader()
    protocol = asyncio.StreamReaderProtocol(reader)
    await loop.connect_read_pipe(lambda: protocol, sys.stdin)
    line = await reader.readline()
    return line.decode().rstrip("\n")

async def chat_client(name, server_ip, port = "8765"):
    async with websockets.connect(f"ws://{server_ip}:{port}") as websocket:
        print(f"Connected as {name}")

        async def send_messages():
            while True:
                msg = await asyncio.get_running_loop().run_in_executor(None, input, "")
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
    server_ip = input("Enter server IP (leave blank to use config): ")
    if not server_ip:
        try:
            with open("config", "r") as f:
                server_ip = f.readline().strip()
                if not server_ip:
                    raise ValueError("Config file is empty.")
                print(f"Loaded server IP from config: {server_ip}")
        except FileNotFoundError:
            print("Config file not found.")
        except Exception as e:
            print(f"Error reading config file: {e}")
    if server_ip:
        asyncio.run(chat_client(name, server_ip))
    else:
        print("No server ip error.")

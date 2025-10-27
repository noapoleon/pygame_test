#!/usr/bin/env python

import asyncio
import websockets
import json

clients = set()

async def handle_client(websocket):
    # Register new clients
    clients.add(websocket)
    print(f"\033[32mClient connected. Total: {len(clients)}\033[0m")

    try:
        async for message in websocket:
            data = json.loads(message)
            sender = data["name"]
            msg = data["msg"]

            print(f"\033[33m{sender}:\033[0m {msg}")
            await broadcast_message(sender, msg, websocket)

    except websockets.ConnectionClosed as e:
        print(f"\033[31mClient Disconnected. {e}\033[0m")
    finally:
        print(f"\033[34mRemaining clients: {len(clients)}\033[0m")
        clients.remove(websocket)

async def broadcast_message(sender, msg, websocket):
    broadcast = json.dumps({"name": sender, "msg": msg})
    dead_clients = []

    for client in clients:
        if client != websocket:
            try:
                await client.send(broadcast)
                print(f"sent -> {client}")
            except websockets.ConnectionClosed:
                dead_clients.append(client)
    for client in dead_clients:
        clients.remove(client)


async def main():
    async with websockets.serve(handle_client, "0.0.0.0", 8765):
        print("Chat server running at ws://0.0.0.0:8765")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())

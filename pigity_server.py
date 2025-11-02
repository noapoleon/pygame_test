#!/usr/bin/env python


import asyncio
import websockets
import json
import uuid
import time

TICK_RATE = 128
TICK_INTERVAL = 1/TICK_RATE
clients = {}
lock = asyncio.Lock

async def handle_client(websocket):
    # init client
    print(type(websocket))
    client_id = str(uuid.uuid4())
    clients[client_id] = {"ws": websocket, "x": 0, "y": 0}
    await websocket.send(json.dumps({"uuid": client_id, "tick_rate": TICK_RATE}))
    # send client its uuid
    print(f"\033[32mClient joined. Total: {len(clients)}\033[0m")

    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                if "x" in data and "y" in data:
                    clients[client_id]["x"] = data["x"]
                    clients[client_id]["y"] = data["y"]
                else:
                    print(f"Invalid message from {client_id}: {data}")
            except json.JSONDecodeError:
                print(f"Invalid JSON from {client_id}: {message}")
    except websockets.ConnectionClosed as e:
        print(f"\033[33mClient Disconnection Error: {e}\033[0m")
    finally:
        del clients[client_id]
        print(f"\033[31mClient left. Total: {len(clients)}\033[0m")

async def broadcast_positions():
    async def safe_send(client: dict, message: str) -> None:
        try:
            await client["ws"].send(message)
        except Exception as e:
            print(f"Broadcast loop client error: {e}")


    next_tick = time.perf_counter()
    while True:
        if clients:
            try:
                # TODO: lock during snapshot creation maybe? if key gets removed by handle_client could cause issues
                snapshot = {cid: {"x": c["x"], "y": c["y"]} for cid, c in clients.items()}
                msg = json.dumps(snapshot)

                await asyncio.gather(*(safe_send(c, msg) for c in clients.values()))
            except Exception as e:
                print(f"Broadcast loop error: {e}")

        # sleep to match tick rate
        next_tick += TICK_INTERVAL
        delay = next_tick - time.perf_counter()
        if delay > 0:
            await asyncio.sleep(delay)
        else:
            next_tick = time.perf_counter()


async def main():
    async with websockets.serve(handle_client, "0.0.0.0", 8765):
        print("Server running on port 8765")
        asyncio.create_task(broadcast_positions()) # runs forever
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())

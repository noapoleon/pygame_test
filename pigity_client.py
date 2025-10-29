#!/usr/bin/env python


import pygame
import asyncio
import websockets
import json

TICK_RATE = 128
TICK_INTERVAL = 1/TICK_RATE

async def main():
    server_ip = ""

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
    async with websockets.connect(f"ws://{server_ip}") as ws:

        # init client
        data = json.loads(await ws.recv())
        if data.get("uuid"):
            client_uuid = data["uuid"]
            print("\033[32mConnected to server\033[0m")
        else:
            print(f"\033[31mServer did not send a valid uuid: {data}\nExiting...\033[0m")
            return
        if data.get("tick_rate"):
            TICK_RATE = data["tick_rate"]
            TICK_INTERVAL = 1/TICK_RATE


        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        clock = pygame.time.Clock()

        players = {}
        players_lock = asyncio.Lock()
        x, y = 0, 0

        async def send_position():
            nonlocal x, y
            while running:
                x, y = pygame.mouse.get_pos()
                msg = json.dumps({"x": x, "y": y})
                await ws.send(msg)
                await asyncio.sleep(TICK_INTERVAL)
                # try:
                #     await websocket.send(json.dumps({"x": x, "y": y}))
                # except websockets.ConnectionClosed as e:
                #     print(f"Server disconnected: {e}")
                #     break

        async def receive_positions():
            nonlocal players
            async for message in ws:
                players = json.loads(message)

        asyncio.create_task(send_position())
        asyncio.create_task(receive_positions())


        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False


            x, y = pygame.mouse.get_pos()
            # Send mouse pos
            #

            # -- Drawing --
            screen.fill((30,30,30))
            pygame.draw.circle(screen, (0, 255, 0), (x,y), 15)
            # Draw peers
            async with players_lock:
                snapshot = dict(players)
            for cid, pos in snapshot.items():
            # for cid, pos in snapshot.items():
                if cid != client_uuid:
                    pygame.draw.circle(screen, (255, 0, 0), (pos["x"], pos["y"]), 15)

            pygame.display.flip()
            await asyncio.sleep(0)
            clock.tick(TICK_RATE)
        pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())

#!/usr/bin/env python


import pygame
import asyncio
import websockets
import json

SERVER_URI = "ws://127.0.0.1:8765"


async def main():
    async with websockets.connect(SERVER_URI) as websocket:
        print("\033[32mConnected to server\033[0m")

        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        clock = pygame.time.Clock()

        players = {}
        x, y = 0, 0

        async def send_position():
            nonlocal x, y
            while running:
                x, y = pygame.mouse.get_pos()
                msg = json.dumps({"x": x, "y": y})
                await websocket.send(msg)
                await asyncio.sleep(1/60)
                # try:
                #     await websocket.send(json.dumps({"x": x, "y": y}))
                # except websockets.ConnectionClosed as e:
                #     print(f"Server disconnected: {e}")
                #     break

        async def receive_positions():
            nonlocal players
            async for message in websocket:
                players = json.loads(message)
                print(players)

        asyncio.create_task(send_position())
        asyncio.create_task(receive_positions())

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False


            x, y = pygame.mouse.get_pos()
            # Send mouse pos

            # -- Drawing --
            screen.fill((30,30,30))
            pygame.draw.circle(screen, (0, 255, 0), (x,y), 15)
            # Draw peers
            for pos in players.values():
                if pos != {"x": x, "y": y}:
                    pygame.draw.circle(screen, (255, 0, 0), (pos["x"], pos["y"]), 15)


            pygame.display.flip()
            await asyncio.sleep(0)
            clock.tick(60)
        pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())

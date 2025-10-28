#!/usr/bin/env python

import asyncio
import time

async def prints():
    while True:
        print("hello")
        await asyncio.sleep(1)
async def prints2():
    while True:
        print("world")
        await asyncio.sleep(1)
async def prints3():
    while True:
        print("", end="")
async def thingy():
    while True:
        print("obnjour")
        await asyncio.sleep(0.1)

async def main():
    await asyncio.gather(
        prints(),
        prints2(),
        thingy()
    )


asyncio.run(main())

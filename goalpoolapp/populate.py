from fpl import FPL

import aiohttp
import asyncio

from models import Player

async def main():
    session = aiohttp.ClientSession()
    fpl = FPL(session)
    players = fpl.elements
    print(len(players))
    for i in range(1, len(players)):
        playerdata = fpl.elements[i]
        player = Player.create(playerdata["web_name"], "null")

        print(player.team)
    await session.close()

asyncio.run(main())

from fpl import FPL

import aiohttp
import asyncio

from goalpoolapp.models import Player

clubs = [
    "Arsenal",
    "Aston Villa",
    "Bournemouth",
    "Brentford",
    "Brighton",
    "Chelsea",
    "Crystal Palace",
    "Everton",
    "Fulham",
    "Leicester",
    "Leeds",
    "Liverpool",
    "Man City",
    "Man Utd",
    "Newcastle",
    "Nott'm Forest",
    "Southampton",
    "Spurs",
    "West Ham",
    "Wolves",
]

def run():
    playerstoadd = []
    async def main():
        session = aiohttp.ClientSession()
        fpl = FPL(session)
        players = fpl.elements
        print(len(players))
        for i in range(1, len(players)):
            playerdata = fpl.elements[i]
            try:
                Player.object.get(name=playerdata["web_name"])
            except:
                name = playerdata["web_name"]
                club = clubs[playerdata["team"]-1]
                goals = playerdata["goals_scored"]
                playerstoadd.append(Player.create(name, club, goals))
        await session.close()
    asyncio.run(main())
    for player in playerstoadd:
        player.save()

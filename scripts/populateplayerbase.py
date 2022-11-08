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
    playerbase = []
    async def main():
        session = aiohttp.ClientSession()
        fpl = FPL(session)
        for i in range(1, len(fpl.elements)):
            playerdata = fpl.elements[i]
            playerbase.append(playerdata)
        await session.close()
    asyncio.run(main())
    for player in playerbase:
        try:
            playerupdate = Player.objects.get(playercode=player["code"])
            # if player["goals_scored"] > playerupdate.goals:
            #     for team in playerupdate.teams.all():
            #         team.totalgoals += player["goals_scored"] - playerupdate.goals
            #     playerupdate.goals = player["goals_scored"]
            #     playerupdate.save()
        except:
            playercode = player["code"]
            firstname = player["first_name"]
            surname = player["second_name"]
            nickname = player["web_name"]
            realteam = clubs[player["team"]-1]
            goals = player["goals_scored"]
            Player.create(playercode, firstname, surname, nickname, realteam, goals).save()
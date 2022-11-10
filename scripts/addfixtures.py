from fpl import FPL

import aiohttp
import asyncio

from goalpoolapp.models import Fixture, Player

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
    fixturesbase = []
    async def main():
        session = aiohttp.ClientSession()
        fpl = FPL(session)
        fixtures = await fpl.get_fixtures()
        for fixture in fixtures:
            fixturesbase.append(fixture)
        await session.close()
    asyncio.run(main())
    for fixture in fixturesbase:
        if fixture.event != None:
            try:
                fixturedata = Fixture.objects.get(code=fixture.code)
            except:
                fixturedata = Fixture.create(fixture.code, fixture.event, fixture.kickoff_time, clubs[fixture.team_h-1], clubs[fixture.team_a-1])
                fixturedata.save()
            if fixture.stats != {}:
                for scorer in fixture.stats['goals_scored']["h"]:
                    player = Player.objects.get(playercode=scorer['element'])
                    player.currentweekgoals = scorer['value']
                    player.save()
                    fixturedata.homescorers.add(player)
                    fixturedata.homescore += scorer['value']
                for scorer in fixture.stats['goals_scored']["a"]:
                    player = Player.objects.get(playercode=scorer['element'])
                    player.currentweekgoals = scorer['value']
                    player.save()
                    fixturedata.awayscorers.add(player)
                    fixturedata.awayscore += scorer['value']
            fixturedata.save()

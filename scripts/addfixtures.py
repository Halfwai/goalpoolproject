from fpl import FPL

import aiohttp
import asyncio

from goalpoolapp.models import Fixture, Player, GlobalVars

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
    fixturesbase = []
    async def main():
        session = aiohttp.ClientSession()
        fpl = FPL(session)
        fixtures = await fpl.get_fixtures()
        for fixture in fixtures:
            fixturesbase.append(fixture)
        for i in range(1, len(fpl.elements)):
            playerdata = fpl.elements[i]
            playerbase.append(playerdata)
        await session.close()
    asyncio.run(main())
    players = Player.objects.all()
    for player in players:
        player.currentweekgoals = 0
        player.save()
    for fixture in fixturesbase:
        if fixture.event != None:
            try:
                fixturedata = Fixture.objects.get(code=fixture.code)
            except:
                fixturedata = Fixture.create(fixture.code, fixture.event, fixture.kickoff_time, clubs[fixture.team_h-1], clubs[fixture.team_a-1])
                fixturedata.save()
            round = GlobalVars.objects.all().first().roundnumber
            if fixture.stats != {}:
                if fixture.event == round:
                    for scorer in fixture.stats['goals_scored']["h"]:
                        player = Player.objects.get(playercode=scorer['element'])
                        player.currentweekgoals = scorer['value']
                        player.save()
                        fixturedata.homescorers.add(player)
                    for scorer in fixture.stats['goals_scored']["a"]:
                        player = Player.objects.get(playercode=scorer['element'])
                        player.currentweekgoals = scorer['value']
                        player.save()
                        fixturedata.awayscorers.add(player)
                fixturedata.homescore = fixture.team_h_score
                fixturedata.awayscore = fixture.team_a_score
            fixturedata.save()
    for player in playerbase:
        try:
            playerupdate = Player.objects.get(playercode=player["code"])
            if player["goals_scored"] > playerupdate.goals:
                for team in playerupdate.teams.all():
                    team.totalgoals += player["goals_scored"] - playerupdate.goals
                playerupdate.goals = player["goals_scored"]
                playerupdate.save()
        except:
            playercode = player["id"]
            firstname = player["first_name"]
            surname = player["second_name"]
            nickname = player["web_name"]
            realteam = clubs[player["team"]-1]
            goals = player["goals_scored"]
            Player.create(playercode, firstname, surname, nickname, realteam, goals).save()

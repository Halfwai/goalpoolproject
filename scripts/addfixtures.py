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
    asyncio.run(main(playerbase, fixturesbase))
    for player in playerbase:
        try:
            updatePlayer(player)
        except:
            createPlayer(player)
    resetGoals()
    for fixture in fixturesbase:
        if fixture.event != None:
            fixturedata = getFixtureData(fixture)
            round = GlobalVars.objects.all().first().roundnumber
            if fixture.stats != {}:
                if fixture.event == round:
                    addCurrentRoundGoals(fixture, fixturedata)
                    fixturedata.save()

async def main(playerbase, fixturesbase):
    async with aiohttp.ClientSession(trust_env=True) as session:
        session = aiohttp.ClientSession()
        fpl = FPL(session)
        fixtures = await fpl.get_fixtures()
        for fixture in fixtures:
            fixturesbase.append(fixture)
        for i in range(1, len(fpl.elements)):
            playerdata = fpl.elements[i]
            playerbase.append(playerdata)
        await session.close()

def updatePlayer(player):
    playerupdate = Player.objects.get(playercode=player["id"])
    if player["goals_scored"] > playerupdate.goals:
        for team in playerupdate.teams.all():
            print(player["goals_scored"] - playerupdate.goals)
            team.totalgoals += player["goals_scored"] - playerupdate.goals
            team.save()
        playerupdate.goals = player["goals_scored"]
        playerupdate.save()

def createPlayer(player):
    playercode = player["id"]
    firstname = player["first_name"]
    surname = player["second_name"]
    nickname = player["web_name"]
    realteam = clubs[player["team"]-1]
    goals = player["goals_scored"]
    Player.create(playercode, firstname, surname, nickname, realteam, goals).save()

def resetGoals():
    players = Player.objects.all()
    for player in players:
        player.currentweekgoals = 0
        player.save()

def getFixtureData(fixture):
    try:
        data = Fixture.objects.get(code=fixture.code)
    except:
        data = Fixture.create(fixture.code, fixture.event, fixture.kickoff_time, clubs[fixture.team_h-1], clubs[fixture.team_a-1])
        data.save()
    return data

def addCurrentRoundGoals(fixture, fixturedata):
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
from goalpoolapp.models import *
import datetime
import pytz

import http.client
import json

# setup API variables
conn = http.client.HTTPSConnection("v3.football.api-sports.io")
headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': "7d5a710b4a4bf25600bcf775ce676204",
    }

# set global variables
fixtures_query = []
game_week = GlobalVars.objects.all().first()
fixtures = Fixture.objects.filter(round=game_week.roundnumber, finished=False)
start_time = datetime.timedelta(hours=0)
end_time = datetime.timedelta(hours=3)
now = datetime.datetime.now(tz=pytz.UTC)
global_league = League.objects.get(id='19')
global_teams = Team.objects.filter(league=global_league).order_by("-totalgoals")

# gets events from a specific fixture
def getFixtureData(code, events):
    conn.request("GET", f"/fixtures/events?fixture={code}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    event_page = json.loads(data)
    for event in event_page['response']:
        events.append(event)
    return events

# Add the goalscorers to the fixture, and adds the goals to the player
def addPlayerGoals(fixture):
    events = []
    fixture_events = getFixtureData(fixture.code, events)
    events_log = {}
    for fixture_event in fixture_events:
        if fixture_event['detail'] == "Normal Goal" or fixture_event['detail'] == "Penalty":
            if fixture_event['player']['id'] not in events_log:
                print("new goalscorer added")
                events_log[fixture_event['player']['id']] = 1
            else:
                print("previous goalscorer updated")
                events_log[fixture_event['player']['id']] += 1
    fixture.homescore = 0
    fixture.awayscore = 0
    for key in events_log.keys():
        player = Player.objects.get(playercode=key)
        player.currentweekgoals = events_log[key]
        if player in fixture.hometeam.players.all():
            fixture.homescorers.add(player)
            fixture.homescore += player.currentweekgoals
        elif player in fixture.awayteam.players.all():
            fixture.awayscorers.add(player)
            fixture.awayscore += player.currentweekgoals
        player.save()
        fixture.save()

# Adds scorers current goals to total goals and tallies up team goals
def addGoalsTotals(fixture):
    homescorers = fixture.homescorers.all()
    awayscorers = fixture.awayscorers.all()
    for player in homescorers:
        player.goals += player.currentweekgoals
        player.save()
        playerteams = player.teams.all()
        for team in playerteams:
            team.totalgoals += player.currentweekgoals
            team.save()
    for player in awayscorers:
        player.goals += player.currentweekgoals
        player.save()
        playerteams = player.teams.all()
        for team in playerteams:
            team.totalgoals += player.currentweekgoals
            team.save()
    fixture.finished = True
    fixture.save()

def run():
    # checks if any games are returned, if not then teams are tallied
    if fixtures:
        for fixture in fixtures:
            if now - fixture.date > start_time and fixture.finished == False:
                print(f"{fixture.hometeam} vs {fixture.awayteam} currently ongoing")
                fixtures_query.append(fixture)
        for fixture in fixtures_query:
            addPlayerGoals(fixture)
        for fixture in fixtures:
            if now - fixture.date > end_time and fixture.finished == False:
                addGoalsTotals(fixture)
    else:
        global_league.transfersAllowed = True
        global_league.save()
        position = 1
        provisional_position = 1
        points_tally = global_teams.first().totalgoals
        print(points_tally)
        for team in global_teams:
            if team.totalgoals == points_tally:
                provisional_position += 1
            else:
                position = provisional_position
            team.rank = position
            provisionalplayers = team.provisionalplayers.all()
            if provisionalplayers:
                team.players.clear()
                for player in provisionalplayers:
                    team.players.add(player)
                team.provisionalplayers.clear()
            team.save()
        next_fixtures = Fixture.objects.filter(round=game_week.roundnumber+1).order_by('date').first()
        if next_fixtures:
            if next_fixtures.date - now < end_time:
                global_league.transfersAllowed = False
                game_week.roundnumber += 1
                game_week.save()


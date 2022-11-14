from goalpoolapp.models import *
import datetime
import pytz

import http.client
import json

conn = http.client.HTTPSConnection("v3.football.api-sports.io")

headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': "7d5a710b4a4bf25600bcf775ce676204",
    }

def getFixtureData(code, events):
    conn.request("GET", f"/fixtures/events?fixture={code}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    eventpage = json.loads(data)
    for event in eventpage['response']:
        events.append(event)
    return events

def addgoals(fixture):
    events = []
    fixtureevents = getFixtureData(fixture.code, events)
    eventslog = {}
    for fixtureevent in fixtureevents:
        if fixtureevent['detail'] == "Normal Goal" or fixtureevent['detail'] == "Penalty":
            if fixtureevent['player']['id'] not in eventslog:
                print("newgoalscorer added")
                eventslog[fixtureevent['player']['id']] = 1
            else:
                print("previous goalscorer updated")
                eventslog[fixtureevent['player']['id']] += 1
    for key in eventslog.keys():
        player = Player.objects.get(playercode=key)
        player.currentweekgoals = eventslog[key]
        player.save()

def run():
    fixturesquery = []
    fixtures = Fixture.objects.all()
    starttime = datetime.timedelta(hours=0)
    endtime = datetime.timedelta(hours=3)
    now = datetime.datetime.now(tz=pytz.UTC)
    for fixture in fixtures:
        if now - fixture.date > starttime and now - fixture.date < endtime:
            print(f"{fixture.hometeam} vs {fixture.awayteam} currently ongoing")
            fixturesquery.append(fixture)
    for fixture in fixturesquery:
        addgoals(fixture)
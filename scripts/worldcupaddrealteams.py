from goalpoolapp.models import Country

import http.client
import json

def run():
    conn = http.client.HTTPSConnection("v3.football.api-sports.io")

    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': "7d5a710b4a4bf25600bcf775ce676204",
        }

    conn.request("GET", "/teams?league=1&season=2022", headers=headers)

    res = conn.getresponse()
    data = res.read()

    teams = json.loads(data)

    for team in teams["response"]:
        print(team['team']["name"], team['team']["logo"], team['team']["id"])
        teamdata = RealTeam.create(team['team']["name"], team['team']["logo"], team['team']["id"])
        teamdata.save()

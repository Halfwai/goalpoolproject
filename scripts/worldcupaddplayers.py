from goalpoolapp.models import Player, Country
from time import sleep

import http.client
import json


conn = http.client.HTTPSConnection("v3.football.api-sports.io")

headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': "7d5a710b4a4bf25600bcf775ce676204",
    }

def getPlayerData(page, playersdata):
    # conn.request("GET", f"/players?league=1&season=2022&page={page}", headers=headers)
    # conn.request("GET", f"/players?team=2&season=2022&page={page}", headers=headers)
    conn.request("GET", "/players/squads?team=9", headers=headers)
    res = conn.getresponse()
    data = res.read()
    players = json.loads(data)
    for player in players["response"][0]["players"]:
        playersdata.append(player)
    teams = players["response"][0]["team"]
    return teams
    # if page < players['paging']['total']:
    #     sleep(1)
    #     getPlayerData(page + 1, playersdata)

def run():
    playersdata = []
    teamdata = getPlayerData(1, playersdata)
    print(teamdata)
    team = Country.objects.get(countryname=teamdata['name'])
    for playerdata in playersdata:
        try:
            player = Player.objects.get(playercode=playerdata["id"])
        except:
            player = Player.create(playerdata["id"],
                playerdata['name'],
                playerdata["photo"],
                playerdata['position'])
            player.country = team
            print(player.nickname)
            player.save()
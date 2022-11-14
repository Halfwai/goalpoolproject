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
    conn.request("GET", f"/players?league=1&season=2022&page={page}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    players = json.loads(data)
    for player in players["response"]:
        playersdata.append(player)
    if page < players['paging']['total']:
        sleep(1)
        getPlayerData(page + 1, playersdata)

def run():
    playersdata = []
    getPlayerData(1, playersdata)
    for playerdata in playersdata:
        try:
            player = Player.objects.get(playercode=playerdata['player']["id"])
        except:
            player = Player.create(playerdata['player']["id"],
                playerdata['player']["firstname"],
                playerdata['player']["lastname"],
                playerdata['player']['name'],
                playerdata['statistics'][0]['goals']['total'],
                playerdata['player']["photo"])
            team = Country.objects.get(countryname=playerdata['player']["nationality"])
            player.country = team
            print(player.nickname)
            player.save()
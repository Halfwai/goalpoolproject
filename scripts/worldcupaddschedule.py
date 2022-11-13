from goalpoolapp.models import Fixture, Country

import http.client
import json
import re


def get_trailing_number(s):
    m = re.search(r'\d+$', s)
    return int(m.group()) if m else None

conn = http.client.HTTPSConnection("v3.football.api-sports.io")

headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': "7d5a710b4a4bf25600bcf775ce676204",
    }

def run():
    conn.request("GET", "/fixtures?league=1&season=2022", headers=headers)

    res = conn.getresponse()
    data = res.read()

    rounds = json.loads(data)

    for round in rounds["response"]:
        roundnumber = get_trailing_number(round['league']['round'])
        hometeam = Country.objects.get(countryid=round['teams']['home']['id'])
        awayteam = Country.objects.get(countryid=round['teams']['away']['id'])
        fixture = Fixture.create(round['fixture']['id'], roundnumber, round['fixture']['date'], hometeam, awayteam)
        fixture.save()
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
        try:
            fixture = Fixture.objects.get(code=round['fixture']['id'])
            fixture.date = round['fixture']['date']
            fixture.save()
        except:
            print(round['league']['round'])
            try:
                roundnumber = get_trailing_number(round['league']['round'])
            except:
                roundnumber = 0
            if roundnumber == 16:
                roundnumber = 4
            if round['league']['round'] == "Quarter-finals":
                roundnumber = 5
            if round['league']['round'] == "Semi-finals":
                roundnumber = 6
            print(roundnumber)
            hometeam = Country.objects.get(countryid=round['teams']['home']['id'])
            awayteam = Country.objects.get(countryid=round['teams']['away']['id'])
            fixture = Fixture.create(round['fixture']['id'], roundnumber, round['fixture']['date'], hometeam, awayteam)
            fixture.save()
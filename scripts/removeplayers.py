from goalpoolapp.models import *

global_league = League.objects.get(id='19')
team = Team.objects.get(id="37")
global_teams = global_league.leagueteams.all()

def run():
    for team in global_teams:
        counter = 0
        for player in team.players.all():
            if counter >= 4:
                team.players.remove(player)
                team.save()
            counter += 1
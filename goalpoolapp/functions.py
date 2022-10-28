from .models import User, Team, League, Player

def checkLeagueCode(code):
    try:
        League.objects.get(leaguecode = code)
        return True
    except:
        return False
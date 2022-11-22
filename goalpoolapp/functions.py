from .models import *

def checkLeagueCode(code):
    try:
        League.objects.get(leaguecode = code)
        return True
    except:
        return False

def getGlobalLeague():
    return League.objects.get(id='19')
# django imports
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse

# python imports
from uuid import uuid4
from fpl import FPL
from random import randint
from json import loads

# app imports
from .models import User, Team, League, Player
from .forms import NewLeagueForm, NewTeamForm
from .functions import checkLeagueCode

# Create your views here.
# base page view
def index(request):
    if not request.user.is_authenticated:
        return render(request, 'goalpoolapp/index.html', {
            'title': "Welcome",
    })
    else:
        return HttpResponseRedirect(reverse("goalpoolapp:dashboard"))

# registers a new user
def register(request):
    # shows register page when method is GET
    if request.method == 'GET':
        return render(request, 'goalpoolapp/register.html')
    # attempts to create and save user then the method is POST
    elif request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # make sure that passwords match
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "goalpoolapp/register.html", {
                "message": "Passwords must match."
            })
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "goalpoolapp/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("goalpoolapp:index"))

# login view, renders the login page, and logs in the user if username and password match User model
def loginuser(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("goalpoolapp:index"))
        else:
            return render(request, "goalpoolapp/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "goalpoolapp/login.html")

# Logs out the user
def logoutuser(request):
    logout(request)
    return HttpResponseRedirect(reverse("goalpoolapp:index"))


# shows dashboard for user
def dashboard(request):
    # displays all the teams and leagues user is a part of
    teams = Team.objects.filter(manager=request.user)
    leagues = League.objects.filter(leagueteams__in=teams)
    players = Player.objects.filter(leagues__in=leagues).order_by('-goals')[:10]
    for player in players:
        print(player.teams.all())
    return render(request, 'goalpoolapp/dashboard.html', {
        "teams": teams,
        "leagues": leagues,
        "players": players
    })

# create a league view, uses NewLEagueForm to create a new league
def createleague(request):
    if request.method == "GET":
        return render(request, 'goalpoolapp/createleague.html', {
            "form": NewLeagueForm(),
        })
    else:
        # sets message as blank
        message = ''
        # gets and checks data from NewleagueForm is valid
        league_form = NewLeagueForm(data=request.POST)
        if league_form.is_valid() and "teamname" in request.POST:
            # creates a League model from form data
            league = league_form.save(commit=False)
            # adds the league administrator as the current user
            league.admin = request.user
            # creates a random 8 digit league code that can be used by others to join a league
            leaguecode = uuid4().hex[:8]
            # checks the leaguecode is unique
            while checkLeagueCode(leaguecode):
                leaguecode = uuid4().hex[:8]
            league.leaguecode = leaguecode
            # saves the league
            league.save()
            # sets initial users team in the league
            teamname = request.POST["teamname"]
            team = Team.create(request.user, league, teamname)
            team.save()
        # runs checks on league_form and sets message for what is missing
        for field in league_form:
            if field.errors:
                message = f"Please input {field.name}"
        # checks that the user inputted a team name
        if "teamname" not in request.POST:
            message = f"Please input team name"
        # if message has been set as an error message returns view with error message displayed
        if message != '':
            return render(request, 'goalpoolapp/createleague.html', {
            "message": message,
            "form": NewLeagueForm(),
            })
        # if everything worked properly returns user to their dashboard
        else:
            return HttpResponseRedirect(reverse("goalpoolapp:index"))

# view for user to join already created league
def joinleague(request):
    if request.method == "GET":
        return render(request, 'goalpoolapp/joinleague.html', {
            "form": NewTeamForm(),
        })
    else:
        # checks and validates newteamform
        team_form = NewTeamForm(data=request.POST)
        if team_form.is_valid:
            team = team_form.save(commit=False)
            # uses leaguecode to try and find league, returns error if leaguecode does not match a league
            try:
                league = League.objects.get(leaguecode=request.POST["leaguecode"])
            except:
                message = "Please input valid league code. Please contact league administrator"
                return render(request, 'goalpoolapp/joinleague.html', {
                    "message": message,
                    "form": NewTeamForm(),
            })
            # checks the user does not already have a team in this league
            leagueteams = league.leagueteams.all()
            for team in leagueteams:
                if request.user == team.manager:
                    message = "Sorry, you already have a team in this league"
                    return render(request, 'goalpoolapp/joinleague.html', {
                        "message": message,
                        "form": NewTeamForm(),
                    })
            # checks the league is not full
            if leagueteams.count() >= league.teamlimit:
                message = "Sorry, this league is full. Please contact league administrator"
                return render(request, 'goalpoolapp/joinleague.html', {
                    "message": message,
                    "form": NewTeamForm(),
                })
            # saves new team in league
            team.league = league
            team.manager = request.user
            team.save()
            return HttpResponseRedirect(reverse("goalpoolapp:index"))

def leagueview(request):
    # displayes all the teams and leagues user is a part of
    teams = Team.objects.filter(manager=request.user)
    leagues = League.objects.filter(leagueteams__in=teams)
    return render(request, 'goalpoolapp/leagueview.html', {
        "teams": teams,
        "leagues": leagues,
    })

def startdraft(request, leagueid):
    league = League.objects.get(id=leagueid)
    # If the draft has not been started sets draft order and starts the league
    if league.draftstarted == False:
        teams = league.leagueteams.all()
        draftnumbers = []
        for i in range(0, len(teams)):
            draftnumbers.append(i)
        for team in teams:
            draftnumber = draftnumbers[randint(0, len(draftnumbers)-1)]
            team.draftnumber = draftnumber + 1
            team.save()
            draftnumbers.remove(draftnumber)
        league.draftstarted = True
        league.save()
    return HttpResponseRedirect(reverse("goalpoolapp:draft", kwargs={"leagueid": leagueid}))

def draft(request, leagueid):
    # gets the league
    league = League.objects.get(id=leagueid)
    teams = league.leagueteams.all()
    playercheck = 0
    for team in teams:
        if team.players.count() == league.teamplayerslimit:
            playercheck += 1
    if playercheck == league.leagueteams.count():
        league.draftcomplete = True
        league.save()
    for team in league.leagueteams.all():
        if team.draftnumber == league.draftposition:
            picker = team.manager
    return render(request, 'goalpoolapp/draft.html', {
        "picker": picker,
        "league": league,
    })


def playersearch(request):
    data = loads(request.body)
    team = data["team"]
    league = League.objects.get(id=data["league"])
    players = Player.objects.filter(realteam=team)
    for player in league.leagueplayers.all():
        players = players.exclude(playercode=player.playercode)
    players = players.values()
    return JsonResponse({'players': list(players)})

def pickplayer(request):
    data = loads(request.body)
    league = League.objects.get(id=data["league"])
    player = Player.objects.get(id=data["player"]["id"])
    for leagueplayer in league.leagueplayers.all():
        if leagueplayer == player:
            return JsonResponse({'message': "Player already picked"})
    team = Team.objects.get(manager=request.user, league=league)
    player.leagues.add(league)
    team.players.add(player)
    player.save()
    team.save()
    if league.draftdecending:
        league.draftposition -= 1
    else:
        league.draftposition += 1
    if league.draftposition == 0:
        league.draftposition += 1
        league.draftdecending = False
    elif league.draftposition > league.leagueteams.count():
        league.draftposition -= 1
        league.draftdecending = True
    league.save()
    message = "Player selection successful"
    checkdraft = 0
    for team in league.leagueteams.all():
        if team.players.count() == league.teamplayerslimit:
            checkdraft += 1
    if checkdraft == league.leagueteams.all().count:
        league.draftcomplete = True
        message = "Draft Complete"
    return JsonResponse({'message': message})




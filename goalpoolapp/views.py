# django imports
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.password_validation import validate_password

# python imports
from uuid import uuid4
from fpl import FPL
from random import randint
from json import loads

# app imports
from .models import *
from .forms import NewLeagueForm, NewTeamForm, ChangePasswordForm
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
        try:
            validate_password(password, user=None, password_validators=None)
        except Exception as exception:
            print(exception)
            return render(request, "goalpoolapp/register.html", {
                "message": exception
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
@login_required
def dashboard(request):
    # displays all the teams and leagues user is a part of
    teams = Team.objects.filter(manager=request.user)
    leagues = League.objects.filter(leagueteams__in=teams)
    leagues = leagues.exclude(id='19')
    global_league_teams = League.objects.get(id='19').leagueteams.all()
    global_team = ""
    for team in global_league_teams:
        if team.manager == request.user:
            global_team = team
    players = Player.objects.filter(leagues__in=leagues).order_by('-goals')[:10]
    currentweek = GlobalVars.objects.first().roundnumber
    currentweekvar = Fixture.objects.filter(round=currentweek).order_by('date')
    nextweek = Fixture.objects.filter(round=(currentweek + 1)).order_by('date')
    return render(request, 'goalpoolapp/dashboard.html', {
        "teams": teams,
        "leagues": leagues,
        "players": players,
        "currentweek": currentweekvar,
        "nextweek": nextweek,
        "globalteam": global_team
    })

# create a league view, uses NewLEagueForm to create a new league
@login_required
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
            teamname = request.POST["teamname"]
            if teamname == "":
                message = f"Please input team name"
                return render(request, 'goalpoolapp/createleague.html', {
                    "message": message,
                    "form": NewLeagueForm(),
                    })
            players = Player.objects.all()
            # creates a League model from form data
            league = league_form.save(commit=False)
            players = Player.objects.all()
            if league.teamlimit * league.teamplayerslimit > len(players):
                return render(request, 'goalpoolapp/createleague.html', {
                    "message": "This league is too large. Try reducing the maximum number of teams, or the players per team",
                    "form": NewLeagueForm(),
                })
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
            return HttpResponseRedirect(reverse("goalpoolapp:index"), {
                "message": "League created successfully. Please share leaguecode: {league.leaguecode} to invite others to your league"
            })

# view for user to join already created league
@login_required
def joinleague(request):
    if request.method == "GET":
        return render(request, 'goalpoolapp/joinleague.html', {
            "form": NewTeamForm(),
        })
    else:
        # checks and validates newteamform
        team_form = NewTeamForm(data=request.POST)
        if team_form.is_valid():
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
            for leagueteam in leagueteams:
                if request.user == leagueteam.manager:
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
        else:
            message = "Please fill out form"
            return render(request, 'goalpoolapp/joinleague.html', {
                "message": message,
                "form": NewTeamForm(),
            })

@login_required
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

@login_required
def draft(request, leagueid=None):
    # gets the league
    userteams = Team.objects.filter(manager=request.user)
    if leagueid != None:
        leagueslist = League.objects.filter(id=leagueid)
    else:
        leagueslist = League.objects.filter(leagueteams__in=userteams)
    leagueslist = leagueslist.exclude(id=19)
    leagues = Paginator(leagueslist, 1)
    page = request.GET.get('page')
    league = leagues.get_page(page)
    picker = None
    try:
        teams = league[0].leagueteams.all()
        playercheck = 0
        for team in teams:
            if team.players.count() == league[0].teamplayerslimit:
                playercheck += 1
        if playercheck == league[0].leagueteams.count():
            league[0].draftcomplete = True
            league[0].save()
        for team in league[0].leagueteams.all():
            if team.draftnumber == league[0].draftposition:
                picker = team.manager
    except:
        pass
    return render(request, 'goalpoolapp/draft.html', {
        "picker": picker,
        "leaguepage": league,
        "leagues": leagues,
    })


@login_required
def playersearch(request):
    data = loads(request.body)
    countryname = data["country"]
    country = Country.objects.get(countryname=countryname)
    league = League.objects.get(id=data["league"])
    players = Player.objects.filter(country=country).order_by('nickname')
    if league.duplicatePlayersAllowed == False:
        for player in league.leagueplayers.all():
            players = players.exclude(playercode=player.playercode)
    try:
        team = Team.objects.get(manager=request.user, league=league)
    except:
        pass
    players = players.values()
    return JsonResponse({'players': list(players), 'leagueid': league.id, 'playerlimit': league.teamplayerslimit})

@login_required
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

@login_required
def globalleague(request):
    if request.method == "GET":
        global_league = League.objects.get(id='19')
        try:
            userteam = Team.objects.get(league=global_league, manager=request.user)
            global_teams = global_league.leagueteams.all().order_by('totalgoals')
            teamorder = Paginator(global_teams, 50)
            page = request.GET.get('page')
            teams = teamorder.get_page(page)
            return render(request, 'goalpoolapp/globalleague.html', {
                "league": global_league,
                "team": userteam,
                "teams": teams
            })
        except:
            return render(request, 'goalpoolapp/globalleague.html')

@login_required
def createglobalteam(request):
    if request.method == "GET":
        global_league = League.objects.get(id='19')
        try:
            userteam = Team.objects.get(league=global_league, manager=request.user)
            return HttpResponseRedirect(reverse("goalpoolapp:globalleague"))
        except:
            return render(request, 'goalpoolapp/createglobalteam.html')
    elif request.method == "POST":
        data = loads(request.body)
        players = data['players']
        teamname = data['teamname']
        global_league = League.objects.get(id='19')
        if teamname == "":
            return JsonResponse({
                'message': "Please input Teamname",
                'route': "createglobalteam"
                })
        if len(players) != global_league.teamplayerslimit:
            return JsonResponse({
                'message': "Player limit not matched",
                'route': "createglobalteam"
                })
        try:
            Team.objects.get(manager=request.user, league=global_league)
            return JsonResponse({
                'message': "Team already registered for global league",
                'route': "globalleague"
                })
        except:
            newteam = Team.create(request.user, global_league, teamname)
            newteam.save()
            for player in players:
                playerdata = Player.objects.get(id=player['id'])
                newteam.players.add(playerdata)
            newteam.save()
            return JsonResponse({
                'message': "Team registered successfully",
                'route': "globalleague"
                })

@login_required
def globaltransfers(request):
    global_league = League.objects.get(id='19')
    userteam = Team.objects.get(league=global_league, manager=request.user)
    if request.method == "GET":
        return render(request, 'goalpoolapp/globaltransfers.html', {
            'league': global_league,
            'team': userteam
        })
    else:
        data = loads(request.body)
        players = data['players']
        if len(players) != global_league.teamplayerslimit:
            return JsonResponse({
                'message': "Player limit not matched",
                'route': "createglobalteam"
                })
        userteam.provisionalplayers.clear()
        playerlist = []
        print(players)
        for player in players:
            playerdata = Player.objects.get(playercode=player)
            playerlist.append(playerdata)
        if global_league.transfersAllowed == False:
            for player in playerlist:
                userteam.provisionalplayers.add(player)
            userteam.save()
            return JsonResponse({
                'message': "Transfers registered, transfers will be confirmed at the end of this game round",
                'route': "globalleague"
                })
        else:
            userteam.players.clear()
            for player in playerlist:
                userteam.players.add(player)
            userteam.save()
            return JsonResponse({
                'message': "Transfers Successful",
                'route': "globalleague"
                })

@login_required
def success(request):
    return render(request, 'goalpoolapp/success.html', {
    })

class settings(PasswordChangeView):
    form_class = ChangePasswordForm
    success_url = reverse_lazy("goalpoolapp:success")
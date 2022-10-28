from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from uuid import uuid4

from .models import User, Team, League, Player
from .forms import NewLeagueForm, NewTeamForm
from .functions import checkLeagueCode

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, 'goalpoolapp/index.html', {
            'title': "Welcome",
    })
    else:
        return HttpResponseRedirect(reverse("goalpoolapp:dashboard"))

def register(request):
    if request.method == 'GET':
        return render(request, 'goalpoolapp/register.html')
    elif request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
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

def logoutuser(request):
    logout(request)
    return HttpResponseRedirect(reverse("goalpoolapp:index"))


def dashboard(request):
    return render(request, 'goalpoolapp/dashboard.html', {
        'title': "Welcome",
    })

def createleague(request):
    if request.method == "GET":
        return render(request, 'goalpoolapp/createleague.html', {
            "form": NewLeagueForm(),
        })
    else:
        message = ''
        league_form = NewLeagueForm(data=request.POST)
        if league_form.is_valid() and "teamname" in request.POST:
            league = league_form.save(commit=False)
            league.admin = request.user
            leaguecode = uuid4().hex[:8]
            while checkLeagueCode(leaguecode):
                leaguecode = uuid4().hex[:8]
            league.leaguecode = leaguecode
            league.save()
            teamname = request.POST["teamname"]
            team = Team.create(request.user, league, teamname)
            team.save()
        for field in league_form:
            if field.errors:
                message = f"Please input {field.name}"
        if "teamname" not in request.POST:
            message = f"Please input team name"
        if message != '':
            return render(request, 'goalpoolapp/createleague.html', {
            "message": message,
            "form": NewLeagueForm(),
            })
        else:
            return HttpResponseRedirect(reverse("goalpoolapp:index"))

def joinleague(request):
    if request.method == "GET":
        return render(request, 'goalpoolapp/joinleague.html', {
            "form": NewTeamForm(),
        })
    else:
        team_form = NewTeamForm(data=request.POST)
        if team_form.is_valid:
            print("yes")
        return HttpResponseRedirect(reverse("goalpoolapp:index"))

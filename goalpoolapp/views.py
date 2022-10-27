from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from random import choice
from string import ascii_uppercase

from .models import User, Team, League, Player
from .forms import NewLeagueForm

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

def newleague(request):
    if request.method == "GET":
        return render(request, 'goalpoolapp/newleague.html', {
            "form": NewLeagueForm(),
        })
    else:
        league_form = NewLeagueForm(data=request.POST)
        for field in league_form:
            if field.errors:
                message = f"Please input {field.name}"
        if league_form.is_valid():
            print('yes')
            # league = league_form.save(commit=False)
            # league.admin = request.user
            # league.leaguecode = "boobs"
            # league.save()
            # league.leaguecode = (choice(ascii_uppercase) for i in range(12))
        # leagueName = request.POST["leaguename"]
        # maxplayers = request.POST["maxplayers"]
        # if "transfers" in request.POST:
        #     transfersactivated = True
        # else:
        #     transfersactivated = False
        # if "duplicates" in request.POST:
        #     duplicatesallowed = True
        # else:
        #     duplicatesallowed = False
        return render(request, 'goalpoolapp/newleague.html', {
            "message": message,
            "form": NewLeagueForm(),
        })
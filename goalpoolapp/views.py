from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from .models import User, Team, League, Player

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
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class User(AbstractUser):
    pass

class League(models.Model):
    teamlimit = models.IntegerField()
    leaguename = models.CharField(max_length=64)
    leaguecode = models.CharField(max_length = 10, blank=True, null=True)
    teamplayerslimit = models.IntegerField(validators=[MaxValueValidator(20), MinValueValidator(1)])
    transfersActivated = models.BooleanField()
    duplicatePlayersAllowed = models.BooleanField()
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="administratedleague")
    draftcomplete = models.BooleanField(default=False)
    draftstarted = models.BooleanField(default=False)
    draftposition = models.IntegerField(default=1)
    draftdecending = models.BooleanField(default=False)

class Player(models.Model):
    leagues = models.ManyToManyField(League, related_name="leagueplayers")
    name = models.CharField(max_length=64)
    goals = models.IntegerField()
    realteam = models.CharField(max_length=64)

    def create(name, realteam, goals):
        player = Player(name=name, realteam=realteam, goals=goals)
        return player

class Team(models.Model):
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name="managedteams")
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name="leagueteams")
    players = models.ManyToManyField(Player, related_name="teams", blank=True)
    teamname = models.CharField(max_length=64)
    totalgoals = models.IntegerField(default=0)
    draftnumber = models.IntegerField(blank=True, null=True)

    def create(manager, league, teamname):
        team = Team(manager=manager, league=league, teamname=teamname)
        return team

    def __str__(self):
        return f"{self.teamname}, {self.manager}, {self.league}"


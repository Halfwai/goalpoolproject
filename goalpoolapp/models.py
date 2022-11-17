from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class User(AbstractUser):
    emailpermission = models.BooleanField(null=True)

class League(models.Model):
    teamlimit = models.IntegerField()
    leaguename = models.CharField(max_length=64)
    leaguecode = models.CharField(max_length = 10, blank=True, null=True)
    teamplayerslimit = models.IntegerField()
    transfersActivated = models.BooleanField(default=False)
    transfersAllowed = models.BooleanField(default=False)
    duplicatePlayersAllowed = models.BooleanField()
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="administratedleague")
    draftcomplete = models.BooleanField(default=False)
    draftstarted = models.BooleanField(default=False)
    draftposition = models.IntegerField(default=1)
    draftdecending = models.BooleanField(default=False)

    def __str__(self):
        return self.leaguename

class Country(models.Model):
    countryname = models.CharField(max_length=20)
    countrypic = models.CharField(max_length=100)
    countryid = models.IntegerField()

    def create(countryname, countrypic, countryid):
        country = Country(countryname=countryname, countrypic=countrypic, countryid=countryid)
        return country

    def __str__(self):
        return self.countryname

class Player(models.Model):
    playercode = models.IntegerField()
    leagues = models.ManyToManyField(League, related_name="leagueplayers", blank=True)
    # firstname = models.CharField(max_length=64)
    # surname = models.CharField(max_length=64)
    nickname = models.CharField(max_length=64)
    goals = models.IntegerField(default=0)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="players")
    currentweekgoals = models.IntegerField(default=0)
    position = models.CharField(max_length=12)
    pic = models.CharField(max_length=100)

    def create(playercode, nickname, pic, position):
        player = Player(playercode=playercode, nickname=nickname, pic=pic, position=position)
        return player

    def __str__(self):
        return self.nickname

class Team(models.Model):
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name="managedteams")
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name="leagueteams")
    players = models.ManyToManyField(Player, related_name="teams", blank=True)
    provisionalplayers = models.ManyToManyField(Player, related_name="provisionalteams", blank=True)
    rank = models.IntegerField(default=1)
    teamname = models.CharField(max_length=64)
    totalgoals = models.IntegerField(default=0)
    draftnumber = models.IntegerField(blank=True, null=True)

    def create(manager, league, teamname):
        team = Team(manager=manager, league=league, teamname=teamname)
        return team

    def __str__(self):
        return f"{self.teamname}, {self.manager}, {self.league}"

class Fixture(models.Model):
    code = models.IntegerField()
    round = models.IntegerField()
    date = models.DateTimeField()
    hometeam = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="homefixture")
    awayteam = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="awayfixture")
    homescore = models.IntegerField(default=0)
    awayscore = models.IntegerField(default=0)
    homescorers = models.ManyToManyField(Player, related_name="homegamesscoredin", blank=True)
    awayscorers = models.ManyToManyField(Player, related_name="awaygamesscoredin", blank=True)
    finished = models.BooleanField(default=False)

    def create(code, round, date, hometeam, awayteam):
        fixture = Fixture(code=code, round=round, date=date, hometeam=hometeam, awayteam=awayteam, )
        return fixture

    def __str__(self):
        return f"{self.hometeam} vs {self.awayteam} on {self.date}"

class GlobalVars(models.Model):
    roundnumber = models.IntegerField(default=1)
    def __str__(self):
        return f"{self.roundnumber}"
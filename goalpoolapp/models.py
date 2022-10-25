from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class League(models.Model):
    teamlimit = models.IntegerField()

class Player(models.Model):
    leagues = models.ManyToManyField(League, related_name="leagueplayers", blank=True)
    name = models.CharField(max_length=64)
    goals = models.IntegerField()
    realteam = models.CharField(max_length=64)

class Team(models.Model):
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name="managedteams")
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name="leagueteams")
    players = models.ManyToManyField(Player, related_name="teams", blank=True)
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}, {self.manager}, {self.league}"


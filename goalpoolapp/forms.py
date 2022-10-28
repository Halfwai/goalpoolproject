from django import forms
from django.forms import ModelForm

from .models import League, Team

class NewLeagueForm(ModelForm):
    class Meta:
        model = League
        fields = ["leaguename", "teamlimit", "teamplayerslimit", "duplicatePlayersAllowed", "transfersActivated", ]

class NewTeamForm(ModelForm):
    class Meta:
        model = Team
        fields = ["teamname", "league",]
from django import forms
from .models import League
from django.forms import ModelForm

class NewLeagueForm(ModelForm):
    class Meta:
        model = League
        fields = ["leaguename", "teamlimit", "teamplayerslimit", "duplicatePlayersAllowed", "transfersActivated", ]
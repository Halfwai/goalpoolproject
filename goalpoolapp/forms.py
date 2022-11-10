from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User

from .models import League, Team

class NewLeagueForm(ModelForm):
    class Meta:
        model = League
        fields = ["leaguename", "teamlimit", "teamplayerslimit", "duplicatePlayersAllowed", "transfersActivated", ]

class NewTeamForm(ModelForm):
    class Meta:
        model = Team
        fields = ["teamname",]

class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')
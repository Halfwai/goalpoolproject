from django.contrib import admin
from .models import User, League, Team, Player

from django.contrib.auth.admin import UserAdmin

# Register your models here.
# class UserAdmin(admin.ModelAdmin):
#     list_display = ("id", "username")

class PlayerInline(admin.TabularInline):
    model = Player.teams.through

class LeaguePlayersInline(admin.TabularInline):
    model = Player.leagues.through

class TeamInline(admin.TabularInline):
    model = Team

class TeamPlayerInline(admin.TabularInline):
    model = Team.players.through

class LeagueAdmin(admin.ModelAdmin):
    list_display = ("leaguename", "id")
    inlines = [TeamInline, LeaguePlayersInline]

class TeamAdmin(admin.ModelAdmin):
    inlines = [PlayerInline]
    list_display = ("teamname", "id")

class PlayerAdmin(admin.ModelAdmin):
    list_display = ("nickname", "id")
    inlines = [TeamPlayerInline]


admin.site.register(User, UserAdmin)
admin.site.register(League, LeagueAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Player, PlayerAdmin)
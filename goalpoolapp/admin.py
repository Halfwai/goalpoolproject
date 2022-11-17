from django.contrib import admin
from .models import *

# from django.contrib.auth.admin import UserAdmin

class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "id")

class PlayerInline(admin.TabularInline):
    model = Player.teams.through

class LeaguePlayersInline(admin.TabularInline):
    model = Player.leagues.through

class TeamInline(admin.TabularInline):
    model = Team

class TeamPlayerInline(admin.TabularInline):
    model = Team.players.through

class CountryPlayersInline(admin.TabularInline):
    model = Player
    ordering = ('position', 'nickname')

class LeagueAdmin(admin.ModelAdmin):
    list_display = ("leaguename", "id")
    inlines = [TeamInline, LeaguePlayersInline]

class TeamAdmin(admin.ModelAdmin):
    inlines = [PlayerInline]
    list_display = ("teamname", "league","id")

class PlayerAdmin(admin.ModelAdmin):
    list_display = ("nickname", "country", "id")
    inlines = [TeamPlayerInline]

class FixtureAdmin(admin.ModelAdmin):
    list_display = ("id", "hometeam", "awayteam", "date")

class GlobalVarsAdmin(admin.ModelAdmin):
    list_display = ("id", "roundnumber")

class CountryAdmin(admin.ModelAdmin):
    list_display = ("id", "countryname")
    inlines = [CountryPlayersInline]

admin.site.register(User, UserAdmin)
admin.site.register(League, LeagueAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Fixture, FixtureAdmin)
admin.site.register(GlobalVars, GlobalVarsAdmin)
admin.site.register(Country, CountryAdmin)
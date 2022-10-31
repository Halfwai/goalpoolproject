from django.contrib import admin
from .models import User, League, Team, Player


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username")

class TeamInline(admin.TabularInline):
    model = Team

class LeagueAdmin(admin.ModelAdmin):
    list_display = ("leaguename", "id")
    inlines = [TeamInline]

class TeamAdmin(admin.ModelAdmin):
    list_display = ("teamname", "id")

class PlayerAdmin(admin.ModelAdmin):
    list_display = ("name", "id")


admin.site.register(User, UserAdmin)
admin.site.register(League, LeagueAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Player, PlayerAdmin)
from django.contrib import admin
from .models import User, League


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username")

class LeagueAdmin(admin.ModelAdmin):
    list_display = ("leaguename", "id")


admin.site.register(User, UserAdmin)
admin.site.register(League, LeagueAdmin)
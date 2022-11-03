from django.urls import path, include

from . import views

app_name = 'goalpoolapp'
urlpatterns = [
    # index view
    path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    # sign up and login views
    path('register', views.register, name='register'),
    path('loginuser', views.loginuser, name='loginuser'),
    path('logoutuser', views.logoutuser, name='logoutuser'),
    # main dashboard view
    path('dashboard', views.dashboard, name='dashboard'),
    # draft league views
    path('createleague', views.createleague, name='createleague'),
    path('joinleague', views.joinleague, name='joinleague'),
    path('leagueview', views.leagueview, name='leagueview'),
    path('startdraft <int:leagueid>', views.startdraft, name='startdraft'),
    path('draft <int:leagueid>', views.draft, name='draft'),
    # global league views
    path('pickplayer', views.pickplayer, name='pickplayer'),
    path('globalleague', views.globalleague, name='globalleague'),
    path('createglobalteam', views.createglobalteam, name='createglobalteam'),
    path('playersearch', views.playersearch, name='playersearch'),
]

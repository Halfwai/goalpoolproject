from django.urls import path, include

from . import views

app_name = 'goalpoolapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('dashboard', views.dashboard, name='dashboard'),
    path('register', views.register, name='register'),
    path('loginuser', views.loginuser, name='loginuser'),
    path('logoutuser', views.logoutuser, name='logoutuser'),
    path('createleague', views.createleague, name='createleague'),
    path('joinleague', views.joinleague, name='joinleague')
]
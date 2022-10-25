from django.urls import path

from . import views

app_name = 'goalpoolapp'
urlpatterns = [
    path('', views.index, name='index'),
]
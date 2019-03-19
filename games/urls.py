"""gameshop URL Configuration
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  re_path(r'^', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  re_path(r'^', Home.as_view(), name='home')
"""
from django.contrib import admin
from django.urls import path, re_path
from . import views
from django.contrib.auth import views as auth_views
#from payments import urls


urlpatterns = [
    path('', views.games, name='games_list'),
    re_path(r'^highscores/', views.highscores, name='games_highscores'),
    re_path(r'^addgame/', views.addgame, name='game_add'),

    # the more basic path must be below, otherwise it will ignore redirect to the wrong one
    re_path(r'^playgame/(?P<gameid>\d+)/', views.playgame, name='game_play'),
    re_path(r'^playgame/',views.playgame,name='game_play_basic'),

    re_path(r'^editgame/(?P<gameid>\d+)', views.editgame, name='game_edit'),
    re_path(r'^editgame/', views.editgame, name='game_edit_base'),

]

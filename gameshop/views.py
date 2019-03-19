from django.core.exceptions import ValidationError
from django.http import Http404, HttpResponse
from django.http import HttpResponseRedirect
from . import models
import json
from gameshop.models import Games, Payments, Gamestate
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse


''' Feedback from Ahmed Beder:
The information about views is good. In addition to that, you might consider following:

Other views as Payment callback, User profile could be useful.
You might want to add “Highest scores” view also.
If you describe your views being accessible both logged in and not.
This is quite useful if you go for the Social media sharing goal, as it allows you to add metadata about the game on the template which is accessible to the crawlers that read the page you share. ogp, open graph tags
'''

def home(request):
    # The page dictionary is passed to the html, that then takes the information that it needs
    page = {}
    page={'title':'Home',}
    page['description']='Welcome to the home page of our Gameshop. This is still a work in progress, so plsease be patient.'

    # cards documentation: https://getbootstrap.com/docs/4.2/components/card/
    cards = []    
    cardlist = ['Login', 'Games', 'Highscores', 'Profile']
    cards = [{'title':'Login','text':'Login to your profile','link': reverse('login') },
                {'title':'Games','text':'Browse games and select ones you wish to buy or to play.','link': reverse('games_list') },
                {'title':'Highscores','text':'Read through the highscores of all the games, and compare your scores to them.','link':reverse('games_highscores')},
                {'title':'Profile','text':'View your profile, edit your information and see what other information you have given us.','link': reverse('user_profile')} ]
    if request.user.is_authenticated:
        cards.pop(0)
    page['cards'] = cards
    page['extras']='''   '''
    if request.user.is_authenticated:
        page['user'] = request.user
    if request.user.groups.filter(name="developers").count() != 0:    
        page['developer'] = 'developer'
    return render(request,"home.html",page)

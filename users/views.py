from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Group
from django.http import Http404, HttpResponse
from django.http import HttpResponseRedirect
from gameshop.models import Games, Payments, Gamestate, Developer, player
from django.shortcuts import render, get_object_or_404, redirect
from gameshop.forms import gameform, signupform
from django.urls import reverse
from django.contrib import messages
from django.urls import reverse
from gameshop.token import account_activation_token
from django.core.mail import  send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
import json

'''Feedback from Ahmed Beder:
For authentication: usage of Django’s auth is a good choice.
Also, If you want to send mail, Heroku has services like sendgrid and mailgun which have free tiers.
'''

def signup(request):
  if request.user.is_authenticated:
    return redirect("/")
  page={}
  if request.user.groups.filter(name="developers").count() != 0:    
    page['developer'] = 'developer'
  if request.method == 'POST':
    form = signupform(request.POST)
    if form.is_valid():
      form.save()
      username = form.cleaned_data["username"]
      user=User.objects.get(username= username)
      if form.cleaned_data["role"] == "developer":
        if Group.objects.filter(name="developers").exists():
          developer_group = Group.objects.get(name="developers")
        else:
          Group.objects.create(name="developers").save()
          developer_group = Group.objects.get(name="developers")
        developer_group.user_set.add(user)
        Developer.objects.create(user=user)
      else:
        player.objects.create(user=user)
      #login(request,user,backend='django.contrib.auth.backends.ModelBackend')
      #messages.add_message(request, messages.SUCCESS, 'thank you for joining our community, Now you can sign in!.')
      current_site = get_current_site(request)
      mail_subject = 'Activate your account.'
      message = render_to_string('users/emailconfirmation.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token':account_activation_token.make_token(user),
            })
      to_email = form.cleaned_data.get('email')
      send_mail(mail_subject, message, 'gameshopproject2019@gmail.com', [to_email],fail_silently=False,)
      messages.add_message(request, messages.SUCCESS, 'Thank you for signing up, please confirm your email then login. ')
      return redirect(reverse('login'))


    else:
      messages.add_message(request, messages.ERROR, 'Sorry your inputes were wrong try to check username, email and match passowrds!')
      return redirect(reverse('user_signup'))
  else:
    form = signupform()
    page["title"]="Sign up!"
    page["form"]=form
    return render(request,"users/signup2.html",page)

@login_required(login_url='login')
def profile(request):
    page={}
    if request.user.groups.filter(name="developers").count() != 0:    
      page['developer'] = 'developer'
    page["title"]="Profile"
    if(player.objects.filter(user=request.user).exists()):
        page["type"]="Player"
        mygames = Gamestate.objects.filter(uid=request.user)
        page['mygames']= mygames
    if(Developer.objects.filter(user=request.user).exists()):
        mygames = Games.objects.filter(owner=request.user)
        page['mygames']= mygames
        page["type"]="Developer"
        if Games.objects.filter(owner=request.user).exists():
            page['developed']=Games.objects.filter(owner=request.user)
    return render(request,"users/profile.html", page)

def logouting (request):
  logout(request)
  return HttpResponseRedirect("/")


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return redirect('home')
    else:
        return HttpResponse('something went wrong please try again.')


def facebook_login(request):
  if request.method =="GET":
    user=request.user
    if player.objects.filter(user=user).exists():
      return redirect(reverse('home'))
    else:
      player.objects.create(user=user).save()
      player_new = player.objects.filter(user=user)
      user = player_new
      messages.add_message(request, messages.SUCCESS, 'Thank you for signing up')
      return redirect("home")
  else:
    return HttpResponse(status=500)
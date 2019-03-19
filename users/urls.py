"""gameshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  re_path(r'^', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  re_path(r'^', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  re_path(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from . import views
from django.contrib.auth import views as auth_views
""" these paths are just random ones that I used to get a basic  """
urlpatterns = [
    path('', views.profile),
    re_path(r'^login/', auth_views.LoginView.as_view(template_name='users/login2.html'), name='login'),
    re_path(r'^signup/', views.signup, name='user_signup'),
    re_path(r'^profile/', views.profile, name='user_profile'),
    re_path(r'^logout/', views.logouting, name='user_logout'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),
    re_path(r'facebook/', views.facebook_login,name='facebook_login'),
    
]

from django.contrib import admin
from django.urls import path, re_path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    re_path(r'^admin/', admin.site.urls),
    path('', views.home),
    re_path(r'^home/', views.home, name='home'),
    re_path(r'^users/', include('users.urls')),
    re_path(r'^games/', include('games.urls')),
    re_path(r'^payment/', include('payments.urls')),
    re_path(r'^oauth/', include('social_django.urls', namespace='social')), 

]

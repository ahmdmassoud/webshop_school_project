from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField

''' Note from Valtteri:
I added a fixture of my database with a developer and a player.
These can be loaded from the gameshopdb.psql file by following the instructions on the following website:
https://www.a2hosting.com/kb/developer-corner/postgresql/import-and-export-a-postgresql-database
Developer: Username = balu Password = bearnecessities1
Player: Username = mowgli  Password = raisedbywolves

'''

class Developer(models.Model):
    def __str__(self):
        return  self.user.username
    user = models.OneToOneField( User, on_delete=models.CASCADE,primary_key=True,)


class player(models.Model):
    def __str__(self):
        return  self.user.username
    user = models.OneToOneField( User, on_delete=models.CASCADE,primary_key=True,)
'''
Feedback from Ahmed Beder:
The usage of Django’s default User model is a good choice.
For the game field, it is almost never the case where you’d need a field that is an array.
Instead, I would recommend using a  model that has a field that references the Game, a field that references the User(Player).
You could use a many to many relationship with the games as well.
'''
class Games(models.Model):
    link = models.URLField()
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, default="this is a description")
    highscore = models.FloatField(null=True, default=0.0)
    tags = JSONField(null=True, default=None, blank=True)
    price = models.FloatField(default=0)
    date_created = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    class Meta:
        ordering = ['name']
    pass


class Gamestate(models.Model):
    uid = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    gameid = models.ForeignKey(Games, on_delete=models.CASCADE, null=True, blank=True)
    score = models.FloatField(default=0.0)

    # This was changed to JSONField to make saving and loading easier
    gamestate = JSONField(null=True, default=None, blank=True)
    options = JSONField(null=True, default=None, blank=True)
    class Meta:
        ordering = ['uid' ]
    pass



'''Feedback from Ahmed Beder:
Payment MODEL
The ‘state’ field would be useful.
It will be helpful to identify if the payment was cancelled, received or still in process.
I would recommend to add a unique secure payment_id field for security reasons.
This could be used to identify the payment and prevent fraud.
For the state of payment consider using enums.

Make sure you test this properly.
Most projects have security holes that reduce points.
Make sure that you can't reuse payments, pay for something else you selected etc.
All-in-all try to break your own product!
'''
class Payments(models.Model):
    payment_id = models.CharField(unique=True, max_length=255, default=timezone.now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET(''), null=True, blank=True)
    game = models.ForeignKey(Games, on_delete=models.SET(''), null=True, blank=True)
    price = models.FloatField()
    state = models.CharField(max_length=255, default='processing')
    date = models.DateTimeField(default=timezone.now)
    class Meta:
        ordering = ['date' ]
    pass

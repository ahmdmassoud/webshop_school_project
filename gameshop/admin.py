from django.contrib import admin
from .models import Games, Gamestate,Payments, Developer, player

admin.site.register(Games)
admin.site.register(Gamestate)
admin.site.register(Payments)
admin.site.register(Developer)
admin.site.register(player)
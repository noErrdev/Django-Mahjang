from django.contrib import admin
from .models import *


class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'room_id', 'game_mode', 'host_id')

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'room')

class TileAdmin(admin.ModelAdmin):
    list_display = ('suite', 'number')
    


# Register your models here.

admin.site.register(Room, RoomAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Tile, TileAdmin)
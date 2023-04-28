from django.db import models
 
class Room(models.Model):
    room_id = models.CharField(max_length=8, unique = True) 
    game_mode = models.BooleanField(default=False)
    
    player1 = models.CharField(max_length=50, default="")
    player2 = models.CharField(max_length=50, default="")
    player3 = models.CharField(max_length=50, default="")
    player4 = models.CharField(max_length=50, default="")
    
    current_player = models.CharField(max_length = 50, default= "")
    zhuangjia = models.CharField(max_length = 50, default= "")
    
    bamboo1 = models.SmallIntegerField(default=4)
    bamboo2 = models.SmallIntegerField(default=4)
    bamboo3 = models.SmallIntegerField(default=4)
    bamboo4 = models.SmallIntegerField(default=4)
    bamboo5 = models.SmallIntegerField(default=4)
    bamboo6 = models.SmallIntegerField(default=4)
    bamboo7 = models.SmallIntegerField(default=4)
    bamboo8 = models.SmallIntegerField(default=4)
    bamboo9 = models.SmallIntegerField(default=4)
    wan1 = models.SmallIntegerField(default=4)
    wan2 = models.SmallIntegerField(default=4)
    wan3 = models.SmallIntegerField(default=4)
    wan4 = models.SmallIntegerField(default=4)
    wan5 = models.SmallIntegerField(default=4)
    wan6 = models.SmallIntegerField(default=4)
    wan7 = models.SmallIntegerField(default=4)
    wan8 = models.SmallIntegerField(default=4)
    wan9 = models.SmallIntegerField(default=4)
    circle1 = models.SmallIntegerField(default=4)
    circle2 = models.SmallIntegerField(default=4)
    circle3 = models.SmallIntegerField(default=4)
    circle4 = models.SmallIntegerField(default=4)
    circle5 = models.SmallIntegerField(default=4)
    circle6 = models.SmallIntegerField(default=4)
    circle7 = models.SmallIntegerField(default=4)
    circle8 = models.SmallIntegerField(default=4)
    circle9 = models.SmallIntegerField(default=4)

   

class Player(models.Model):
    player_id = models.CharField(max_length=50, unique=True)
    
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='player_set', null=True)
    
    bamboo1 = models.SmallIntegerField(default=0)
    bamboo2 = models.SmallIntegerField(default=0)
    bamboo3 = models.SmallIntegerField(default=0)
    bamboo4 = models.SmallIntegerField(default=0)
    bamboo5 = models.SmallIntegerField(default=0)
    bamboo6 = models.SmallIntegerField(default=0)
    bamboo7 = models.SmallIntegerField(default=0)
    bamboo8 = models.SmallIntegerField(default=0)
    bamboo9 = models.SmallIntegerField(default=0)
    wan1 = models.SmallIntegerField(default=0)
    wan2 = models.SmallIntegerField(default=0)
    wan3 = models.SmallIntegerField(default=0)
    wan4 = models.SmallIntegerField(default=0)
    wan5 = models.SmallIntegerField(default=0)
    wan6 = models.SmallIntegerField(default=0)
    wan7 = models.SmallIntegerField(default=0)
    wan8 = models.SmallIntegerField(default=0)
    wan9 = models.SmallIntegerField(default=0)
    circle1 = models.SmallIntegerField(default=0)
    circle2 = models.SmallIntegerField(default=0)
    circle3 = models.SmallIntegerField(default=0)
    circle4 = models.SmallIntegerField(default=0)
    circle5 = models.SmallIntegerField(default=0)
    circle6 = models.SmallIntegerField(default=0)
    circle7 = models.SmallIntegerField(default=0)
    circle8 = models.SmallIntegerField(default=0)
    circle9 = models.SmallIntegerField(default=0)


    
#TODO: add more fields and function     
# class Game(models.Model):
#     room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
#     is_finished = models.SmallIntegerField(default=0)
    

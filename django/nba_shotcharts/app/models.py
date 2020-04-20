from django.db import models

# Create your models here.
class Season(models.Model):
    YEAR = models.CharField(primary_key=True, max_length=25)

class Player_id(models.Model):
    PLAYER_ID = models.CharField(max_length=25)
    PLAYER_NAME = models.CharField(max_length=100)
    TEAM_ID = models.CharField(max_length=100)
    TEAM_ABBREVIATION = models.CharField(max_length=25)
    AGE = models.CharField(max_length=25)
    SEASON = models.ForeignKey(Season, on_delete=models.CASCADE, max_length=25)

class Shot_data(models.Model):
    PLAYER_ID = models.CharField(max_length=25)
    SHOT_DISTANCE = models.IntegerField()
    LOC_X = models.IntegerField()
    LOC_Y = models.IntegerField()
    SHOT_ATTEMPTED_FLAG = models.IntegerField()
    SHOT_MADE_FLAG = models.IntegerField()
    ZONE_NAME = models.CharField(max_length=50)
    ACCURACY_FROM_ZONE = models.FloatField()
    TOTALS = models.CharField(max_length=25)
    SEASON = models.ForeignKey(Season, on_delete=models.CASCADE, max_length=25)

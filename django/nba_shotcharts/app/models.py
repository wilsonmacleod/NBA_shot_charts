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
# FIXTURE FORMAT
# "model": "app.Player_id",
#     "fields": {
#        "PLAYER_ID": "", str
#        "PLAYER_NAME": "", str
#         "TEAM_ABBREVIATION": , str
#          "AGE": "", str
#          "SEASON": "", FOREIGNKEY
#         }

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
# FIXTURE FORMAT
# "model": "app.Shot_data"
#     "fields": {
#        "PLAYER_ID": "", str
#        "LOC_X": "", int
#         "LOC_Y": , int
#          "SHOT_ATTEMPTED_FLAG": "", int
#          "SHOT_MADE_FLAG": "", int
#           "ZONE_NAME": "" str
#           "ACCURACY_FROM_ZONE": float
#            "TOTALS": str,
#           "SEASON": "", FOREIGNKEY
#         }
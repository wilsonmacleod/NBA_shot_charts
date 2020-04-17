from django.db import models

# Create your models here.
class Season(models.Model):
    YEAR = models.CharField(primary_key=True, max_length=25)

class Player_id(models.Model):
# FIXTURE FORMAT
# "model": "app.Player_id",
#     "fields": {
#        "PLAYER_ID": "", str
#        "PLAYER_NAME": "", str
#         "TEAM_ABBREVIATION": , str
#          "AGE": "", str
#          "SEASON": "", FOREIGNKEY
#         }
    PLAYER_ID = models.CharField(max_length=25)
    PLAYER_NAME = models.CharField(max_length=100)
    TEAM_ID = models.CharField(max_length=100)
    TEAM_ABBREVIATION = models.CharField(max_length=25)
    AGE = models.CharField(max_length=25)
    SEASON = models.ForeignKey(Season, on_delete=models.CASCADE, max_length=25)

class Shot_data(models.Model):
# FIXTURE FORMAT
# "model": "app.Shot_data"
#     "fields": {
#        "PLAYER_ID": "", str
#        "LOC_X": "", str
#         "LOC_Y": , str
#          "SHOT_ATTEMPTED_FLAG": "", str
#          "SHOT_MADE_FLAG": "", str
#           "ZONE_NAME": "" str
#           "ACCURACY_FROM_ZONE": str
#           "SEASON": "", FOREIGNKEY
#         }
    PLAYER_ID = models.CharField(max_length=25)
    SHOT_DISTANCE = models.IntegerField()
    LOC_X = models.IntegerField()
    LOC_Y = models.IntegerField()
    SHOT_ATTEMPTED_FLAG = models.IntegerField()
    SHOT_MADE_FLAG = models.IntegerField()
    ZONE_NAME = models.CharField(max_length=50)
    ACCURACY_FROM_ZONE = models.IntegerField()
    SEASON = models.ForeignKey(Season, on_delete=models.CASCADE, max_length=25)

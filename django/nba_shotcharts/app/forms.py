from django import forms

from .models import Season, Player_id

class PlayerSelect(forms.Form):
    # init form choices
    def initialize_form(season):
        if len(season) > 0:
            pull_choices = Player_id.objects.filter(SEASON=season).all() # Pull all players from season
            choices = [(str(i.PLAYER_ID) ,str(i.PLAYER_NAME)) for i in pull_choices]
            choices.insert(0, ('Def', 'Select A Player'))
        else:
            choices = [('Def, Select A Season')]
        return choices
    
    # fields
    available_players = forms.ChoiceField(
        choices=[]
    )
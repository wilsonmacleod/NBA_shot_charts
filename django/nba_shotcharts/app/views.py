from django.shortcuts import render

from .models import Season, Player_id
from .forms import PlayerSelect
from .create_charts import Return_Data_and_Charts
# Create your views here.

def base(request):
    seasons = Season.objects.all()
    season_choices = [i.YEAR for i in seasons]
    context={
        'season_choices': season_choices
    }
    return render(request, 'base.html', context)


def player_view(request, season):
    #Shot_data.objects.all().delete()
    
    seasons = Season.objects.all()
    season_choices = [i.YEAR for i in seasons]

    init_state = { # React???
        'season': season,
        'pid': '',
        'show_chart': False
    }
    #FORMS
    player_select = PlayerSelect()
    player_select.fields['available_players'].choices = PlayerSelect.initialize_form(init_state['season']) #set players from season as choices

    #FORM ACTIONS
    if request.GET and init_state['season'] != '':
        init_state['pid'] = request.GET['available_players']
        init_state['show_chart'] = True

    # SET DISPLAY
    if init_state['show_chart']:
        player_details, obj, chart = Return_Data_and_Charts.main(init_state['pid'], init_state['season'])
    else:
        player_details = ''
        obj = ''
        chart = ''

    context = {
        'season_choices': season_choices,
        'player_select': player_select,
        'player_details': player_details,
        'most_att': obj['most_attempted_zone'],
        'highest_acc': obj['highest_accuracy_zone'],
        'avg_dist': obj['average_distance'],
        'season': season,
        'chart': chart
    }

    return render(request, 'player_view.html', context)



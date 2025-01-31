from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q

from .models import Season, Player_id
from .forms import PlayerSelect
from .create_charts import create_charts as cc


def home(request): # home page with search bar
    seasons = Season.objects.all()
    season_choices = [i.YEAR for i in seasons]
    context = {
        'season_choices': season_choices
    }
    return render(request, 'home.html', context)


def player_view(request, season, pid=None, chart_type='default'): # main view
    seasons = Season.objects.all()
    season_choices = [i.YEAR for i in seasons]
    show_chart = False

    # FORMS
    player_select = PlayerSelect()
    player_select.fields['available_players'].choices = PlayerSelect.initialize_form(
        season)  # set players from season as choices

    # FORM ACTIONS
    if request.GET and season != '' and request.GET['available_players'] != 'Def':
        pid = request.GET['available_players']
        show_chart = True
    if pid != 'None':
        pid = pid
        show_chart = True

    # SET DISPLAY
    if show_chart:
        try:
            player_details, obj, chart = cc.main(pid, season, chart_type)
            most_att = obj['most_attempted_zone']
            highest_acc = obj['highest_accuracy_zone']
            avg_dist = obj['average_distance']
        except AttributeError: # if no data found for this player id for this season
            selected = season_choices.index(season)
            back = season_choices[selected - 1]
            messages.warning(request, f'No data for this player for {season}.')
            return redirect('player_view', season=back, pid=pid, chart_type=chart_type)
        except: # safety
            messages.warning(request, f'Something went wrong.')
            return redirect('base')
    else:
        player_details = ''
        most_att = ''
        highest_acc = ''
        avg_dist = ''
        chart = ''

    context = {
        'season_choices': season_choices,
        'player_select': player_select,
        'player_details': player_details,
        'most_att': most_att,
        'highest_acc': highest_acc,
        'avg_dist': avg_dist,
        'season': season,
        'chart': chart,
        'chart_type': chart_type
    }

    return render(request, 'player_view.html', context)


def next_season(request, season, pid, chart_type): # move to next season using same player id and chart view
    try:
        seasons = Season.objects.all()
        season_choices = [i.YEAR for i in seasons]
        current = season_choices.index(season)
        next_season = season_choices[current + 1]
        return redirect('player_view', season=next_season, pid=pid, chart_type=chart_type)
    except:
        return redirect('base')


def search(request): # search func
    query = request.GET.get('q')
    if query:
        results = Player_id.objects.filter(
            Q(PLAYER_NAME__icontains=query)).order_by('-SEASON')[:42]
    else:
        messages.warning(request, f'No search entered.')
        return redirect('home')

    seasons = Season.objects.all()
    season_choices = [i.YEAR for i in seasons]

    results = results if len(results) >= 1 else 'None'
    
    context = {
        'results': results,
        'season_choices': season_choices
    }
    return render(request, 'search.html', context)


def redirect_catch_all(request, path): # redirect URL typos
    return redirect('home')

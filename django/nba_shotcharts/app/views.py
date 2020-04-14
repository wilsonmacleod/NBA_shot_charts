from django.shortcuts import render
from .models import Season, Player_id, Shot_data
# Create your views here.

def home(request):
    obj = Shot_data.objects.filter(SEASON='2010-11').filter(PLAYER_ID='202412').first()
    ppid = obj.PLAYER_ID
    p_obj = Player_id.objects.filter(SEASON='2010-11').filter(PLAYER_ID=ppid).first()

    context = {
        'banner': p_obj.PLAYER_NAME
    }
    return render(request, 'index.html', context)
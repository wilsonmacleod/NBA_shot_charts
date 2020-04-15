from django.shortcuts import render
from .models import Season, Player_id
from .create_charts import Return_Data_and_Charts
# Create your views here.

def home(request):
    x, y = Return_Data_and_Charts.main('2544', '2010-11')
    context = {
        'x': x,
        'y': y
    }
    return render(request, 'index.html', context)
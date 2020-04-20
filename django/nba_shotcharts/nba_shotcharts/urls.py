from django.contrib import admin
from django.urls import path

from app.views import base, search, player_view, next_season

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'', base, name="base"),
    path(f'search/', search, name="search"),
    path(f'player_view/<season>/<pid>/<chart_type>', player_view, name="player_view"),
    path(f'next_season/<season>/<pid>/<chart_type>', next_season, name="next_season"),
    ]

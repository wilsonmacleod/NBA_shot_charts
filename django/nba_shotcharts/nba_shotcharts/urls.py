from django.contrib import admin
from django.urls import path, re_path

from app.views import home, search, player_view, next_season, redirect_catch_all

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'/', home, name="home"),
    path(f'search/', search, name="search"),
    path(f'player_view/<season>/<pid>/<chart_type>', player_view, name="player_view"),
    path(f'next_season/<season>/<pid>/<chart_type>', next_season, name="next_season"),
    re_path(r'^(?P<path>.*)$', redirect_catch_all, name="redirect_catch_all"),
    path('', redirect_catch_all, name="redirect_catch_all"),
    ]

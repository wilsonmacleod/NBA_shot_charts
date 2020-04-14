from django.contrib import admin

from app.models import (
    Season,
    Player_id,
    Shot_data
)
# Register your models here.
admin.site.register(Season)
admin.site.register(Player_id)
admin.site.register(Shot_data)

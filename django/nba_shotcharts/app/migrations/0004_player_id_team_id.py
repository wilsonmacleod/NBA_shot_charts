# Generated by Django 2.2.4 on 2020-04-14 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20200414_0953'),
    ]

    operations = [
        migrations.AddField(
            model_name='player_id',
            name='TEAM_ID',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]

# Generated by Django 4.0 on 2022-01-09 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simPage', '0003_alter_tennisplayer_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='tennisplayer',
            name='drawNum',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]

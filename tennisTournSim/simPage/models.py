from django.db import models

# Create your models here.

class tennisPlayer(models.Model):
    name = models.TextField(unique= True)
    utr = models.FloatField()
    
#python manage.py makemigrations
#python manage.py sqlmigrate simPage 0001
#python manage.py migrate
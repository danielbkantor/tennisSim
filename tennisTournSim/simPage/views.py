from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings 
from .models import tennisPlayer
import csv, requests, os

# Create your views here.

def index(request):
    drawNum = 0
    countNum = 0
    
    with open(os.path.join(settings.BASE_DIR, 'tournament.csv')) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row in csv_reader:
            
            if(countNum != 0 and countNum %2 == 0):
                drawNum += 1
            
            getName = requests.get('https://app.universaltennis.com/api/v2/search/players?query={}&top=1'.format(row))
            responseName = getName.json()
            id = (responseName['hits'][0]['source']['id'])
            response = requests.get('https://app.universaltennis.com/api/v1/player/{}'.format(id))
            playerdata = response.json()
            playerInfo = tennisPlayer()
            playerInfo.name = playerdata['firstName'] + " " +  playerdata['lastName']
            playerInfo.utr = playerdata['singlesUtr']
            playerInfo.drawNum = drawNum
            
            if not tennisPlayer.objects.filter(name = playerInfo.name).exists():
                playerInfo.save()
            
            countNum += 1
                        
    return render(request, 'home.html', {
        "playerlist": tennisPlayer.objects.all()
    })
    
            
            
def computeWinner(request, playerlist):
    tennisPlayer.objects.get()

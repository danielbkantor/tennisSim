from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings 
from .models import tennisPlayer, Matches
import csv, requests, os

# Create your views here.

def index(request):
    drawNum = 0
    countNum = 0
    drawSize = 4
    roundCounter = 1
    
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
            
        initalMatches(request)         
        
        while(drawSize != 1):
            roundCounter = computeResults(request, roundCounter)
            drawSize = drawSize / 2
        
        
    return render(request, 'home.html', {
        "winnerList": Matches.objects.all(),
        "playerlist": tennisPlayer.objects.all()
    })
    
def initalMatches(request):
    count = 0
    while count < 4:
        matchData = Matches()
        list = tennisPlayer.objects.filter(drawNum = count)
        playerOne = list[0]
        playerTwo = list[1]
        if(playerOne.utr > playerTwo.utr):
            matchData.winnerPlayer = playerOne.name
            matchData.loserPlayer = playerTwo.name
            matchData.round = 1
        else:
            matchData.winnerPlayer = playerTwo.name
            matchData.loserPlayer = playerOne.name
            matchData.round = 1
        matchData.save()
        count += 1
           
def computeResults(request, roundCounter):
    list = Matches.objects.filter(round = roundCounter)
    roundCounter += 1
    for playerMatch, playerMatch2 in zip(*[iter(list)]*2):
        playerOneInfo = tennisPlayer.objects.get(name = playerMatch.winnerPlayer)
        playerTwoInfo = tennisPlayer.objects.get(name = playerMatch2.winnerPlayer)
        matchData = Matches()
        if(playerOneInfo.utr > playerTwoInfo.utr):
            matchData.winnerPlayer = playerOneInfo.name
            matchData.loserPlayer = playerTwoInfo.name
            matchData.round = roundCounter
        else:
            matchData.winnerPlayer = playerTwoInfo.name
            matchData.loserPlayer = playerOneInfo.name
            matchData.round = roundCounter
        matchData.save()
        
    return roundCounter


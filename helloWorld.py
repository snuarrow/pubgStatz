import requests
import json
import datetime
from flows import WebDataBasePopulator
from flows import LocalDataBasePopulator
from api import API

#api = API()
#api.__init__()

LocalDataBasePopulator = LocalDataBasePopulator('json')

#webDataBasePopulator = WebDataBasePopulator()
#webDataBasePopulator.saveAllMatchesOfPlayer("JantevaVarsi")

# do magic and print csv points for time spent before landing and rank
#results = set()
#for duoSanhok in filterMatchDataByGameMode("duo-fpp", getMatchesByMap("Savage_Main", getMatchIdsOfPlayer("JantevaVarsi"))):
#    parseContedersFromMatchData(duoSanhok)
#    crawlLandingTimes(getFullTelemetryByMatchData(duoSanhok))

#    for contender in contenders:
#        c = contenders[contender]
#        if c.landingTime != "":
#            land = datetime.datetime.strptime(c.landingTime, '%Y-%m-%dT%H:%M:%S.%fZ')
#            start = datetime.datetime.strptime(duoSanhok["data"]["attributes"]["createdAt"], '%Y-%m-%dT%H:%M:%SZ')
#            patience = land - start
#            print(str(patience.total_seconds())+","+str(c.rank))
    
#    # reset player list
#    contenders = dict()

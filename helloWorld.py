import requests
import json
import datetime

class Contender:
    def __init__(self, id, name, rank):
        #self.matchId = matchId
        self.id = id
        self.name = name
        self.rank = rank

    jumpTime = "" # not used currently
    landingTime = ""

contenders = dict()

def parseContedersFromMatchData(matchData):
    for it in matchData["included"]:
        if 'type' in it and it["type"] == "participant":
            contenders[it["attributes"]["stats"]["name"]] = Contender(
                it["id"],
                it["attributes"]["stats"]["name"],
                it["attributes"]["stats"]["winPlace"]
            )

def getMatchData(matchId):
    url = "https://api.pubg.com/shards/pc-eu/matches/"+matchId
    header = {
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI0YTM4OGMzMC0zMmEwLTAxMzctNDIwZS0wMDU3NDUzNGQzNjMiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTUzNjc4Nzc0LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6Ii1hMjUwZjI0MS1hNGQ2LTRjZDgtOTE3NS04MGY3NGEyY2U3M2YifQ.tAMnseoVOXvOmzvUejT_cnScFC0PyaAPwZL1u4KBrUE",
        "Accept": "application/vnd.api+json"
    }
    return requests.get(url, headers=header).json()

def getMatchIdsOfPlayer(playerName):
    url = "https://api.pubg.com/shards/steam/players?filter[playerNames]="+playerName
    header = {
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI0YTM4OGMzMC0zMmEwLTAxMzctNDIwZS0wMDU3NDUzNGQzNjMiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTUzNjc4Nzc0LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6Ii1hMjUwZjI0MS1hNGQ2LTRjZDgtOTE3NS04MGY3NGEyY2U3M2YifQ.tAMnseoVOXvOmzvUejT_cnScFC0PyaAPwZL1u4KBrUE",
        "Accept": "application/vnd.api+json"
    }
    r = requests.get(url, headers=header)
    return list(map(lambda x: x["id"], r.json()["data"][0]["relationships"]["matches"]["data"]))

def filterMatchDataByGameMode(gameMode, matchDatas):
    return list(filter(lambda x: x["data"]["attributes"]["gameMode"] == gameMode, matchDatas))

def getMatchesByMap(mapName, matchIds):
    return list(
        filter(
            lambda x: x["data"]["attributes"]["mapName"] == mapName,
            list(
                map(lambda x: getMatchData(x), matchIds)
            )
        )
    )

def getUrlFromMatchData(matchData):
    for it in matchData["included"]:
        if 'URL' in it["attributes"]:
            return it["attributes"]["URL"]
    return "de nada"

def getFullTelemetryByMatchData(matchData):
    url = getUrlFromMatchData(matchData)
    return requests.get(url).json()
    
def crawlLandingTimes(telemetryData):
    for it in telemetryData:
        if '_T' in it:
            if it["_T"] == "LogParachuteLanding":
                name = it["character"]["name"]
                contenders[name].landingTime = it["_D"]

# do magic and print csv points for time spent before landing and rank
results = set()
for duoSanhok in filterMatchDataByGameMode("duo-fpp", getMatchesByMap("Savage_Main", getMatchIdsOfPlayer("JantevaVarsi"))):
    parseContedersFromMatchData(duoSanhok)
    crawlLandingTimes(getFullTelemetryByMatchData(duoSanhok))

    for contender in contenders:
        c = contenders[contender]
        if c.landingTime != "":
            land = datetime.datetime.strptime(c.landingTime, '%Y-%m-%dT%H:%M:%S.%fZ')
            start = datetime.datetime.strptime(duoSanhok["data"]["attributes"]["createdAt"], '%Y-%m-%dT%H:%M:%SZ')
            patience = land - start
            print(str(patience.total_seconds())+","+str(c.rank))
    
    # reset player list
    contenders = dict()

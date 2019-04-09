import requests
from parseTool import ParseTool
import json
import datetime

# header = {
#    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI0YTM4OGMzMC0zMmEwLTAxMzctNDIwZS0wMDU3NDUzNGQzNjMiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTUzNjc4Nzc0LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6Ii1hMjUwZjI0MS1hNGQ2LTRjZDgtOTE3NS04MGY3NGEyY2U3M2YifQ.tAMnseoVOXvOmzvUejT_cnScFC0PyaAPwZL1u4KBrUE",
#    "Accept": "application/vnd.api+json"
# }

class Interwebs:

    parseTool = ParseTool()

    def __init__(self, auth):
        self.header = {
            "Authorization": "\""+auth+"\"",
            "Accept": "application/vnd.api+json"
        }

    def webGetMatchData(self, matchId):
        url = "https://api.pubg.com/shards/pc-eu/matches/"+matchId
        return requests.get(url, headers=self.header).json()

    def webGetMatchIdsOfPlayer(self, playerName):
        url = "https://api.pubg.com/shards/steam/players?filter[playerNames]="+playerName
        r = requests.get(url, headers=self.header)
        return list(map(lambda x: x["id"], r.json()["data"][0]["relationships"]["matches"]["data"]))

    def webGetFullTelemetryByMatchData(self, matchData):
        url = self.parseTool.getUrlFromMatchData(matchData)
        return requests.get(url).json()

    def webGetMatchesByMap(self, mapName, matchIds):
        return list(
            filter(
                lambda x: x["data"]["attributes"]["mapName"] == mapName,
                list(
                    map(lambda x: self.webGetMatchData(x), matchIds)
                )
            )
        )
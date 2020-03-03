from dbHandle import DBHandle
from interwebs import Interwebs
from fileIO import JsonReader
import json
import os

class WebDataBasePopulator:
    def __init__(self):
        self.db = DBHandle("localhost", "5432", "pubgstatz", "pubgstatz", "pubgstatz")
        self.interwebs = Interwebs(token=os.environ.get('PUBG_TOKEN'))

    def saveAllMatchesOfPlayer(self, playerName):
        matchIds = self.interwebs.webGetMatchIdsOfPlayer(playerName)
        for matchId in matchIds:
            if not self.db.matchExists(matchId=matchId):
                print(f'downloading match: {matchId}')
                matchJson = self.interwebs.webGetMatchData(matchId)
                self.db.saveMatch(matchId, matchJson)


    def getTelemetriesForExistingMatches(self):
        status, matches = self.db.loadAllMatches()
        for match in matches:
            if not self.db.telemetryExists(matchId=match['matchId']):
                print(f'downloading telemetry for: {match["matchId"]}')
                matchTelemetry = self.interwebs.webGetFullTelemetryByMatchData(match['matchData'])
                if matchTelemetry:
                    self.db.saveTelemetry(matchId=match['matchId'], telemetry=matchTelemetry)
            #else:
                #print(f'{match["matchId"]} already exists')

class LocalDataBasePopulator:
    def __init__(self, relativeFolder: str):
        self.db = DBHandle("localhost", "5432", "pubgstatz", "pubgstatz", "pubgstatz")
        jsonReader = JsonReader(relativeFolder)
        telemetryJsons = jsonReader.telemetryJsons
        for telemetry in telemetryJsons:
            self.db.saveTelemetry(telemetry.matchId, telemetry.json)


class DataLoader:
    def __init__(self):
        self.db = DBHandle("localhost", "5432", "pubgstatz", "pubgstatz", "pubgstatz")

    def loadUniquePlayers(self):
        return [x for x in self.db.loadData(
            #'select': f"data -> 'data' -> 'attributes' -> 'mapName'",
            #'select': f"data",
            #'where': f"data -> 'data' -> 'attributes' ->> 'mapName' = 'Summerland_Main'"
            #'select': f"data -> 'included' -> "
            f"select participant ->> 'id', participant -> 'attributes' -> 'stats' ->> 'name' from (select json_array_elements(data->'included') from matches) as json_object(participant) where participant ->> 'type' = 'participant'"
            #f"select json_array_elements(data->'included') ->> 'id' as participant from matches"
        )]


    def loadTelemetryEvents(self):
        return self.db.loadData(
            "select data from telemetries limit 1"
        )

    def loadAllParachuteLandings(self, mapName: str):
        return [x[0] for x in self.db.loadData(
            #f"select event -> 'character' -> 'location' from (select json_array_elements(data) from telemetries) as json_object(event) where event ->> '_T'='LogParachuteLanding'"
            f"select event -> 'character' -> 'location' from (select json_array_elements(data) from telemetries where id in (select id from matches where data -> 'data' -> 'attributes' ->> 'mapName'='{mapName}' and data -> 'data' -> 'attributes' ->> 'gameMode'='squad-fpp')) as json_object(event) where event ->> '_T'='LogParachuteLanding'"
        )]

# all _T events from karakin # select json_array_elements(data) from telemetries where id in (select id from matches where data -> 'data' -> 'attributes' ->> 'mapName'='Summerland_Main')

class LocalOperations:
    def parseJumpdistanceVsRank(self, relativeFolder):
        print('lol')
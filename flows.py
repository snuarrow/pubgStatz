from dbHandle import DBHandle, getQueryString
from interwebs import Interwebs
from fileIO import JsonReader
import json
import os
from immutables import gameModes, mapNames, db_host
import time

class WebDataBasePopulator:
    def __init__(self):
        self.db = DBHandle(db_host, "5432", "pubgstatz", "pubgstatz", "pubgstatz")
        self.interwebs = Interwebs(token=os.environ.get('PUBG_TOKEN'))
        self.dataloader = DataLoader()

    def saveAllMatchesOfPlayer(self, playerName):
        print(playerName)
        try:
            matchIds = self.interwebs.webGetMatchIdsOfPlayer(playerName)
        except requests.exceptions.ConnectionError as e:
            print(e)
            print(f'connection error, webGetMatchIdsOfPlayer: {playerName}')
        print(f'found: {len(matchIds)} matches')
        for matchId in matchIds:
            if not self.db.matchExists(matchId=matchId):
                print(f'downloading match: {matchId}')
                matchJson = self.interwebs.webGetMatchData(matchId)
                self.db.saveMatch(matchId, matchJson)
            else:
                print(f'match exists: {matchId}')


    def getTelemetriesForExistingMatches(self):
        #status, matches = self.db.loadAllMatches()
        all_match_ids = self.dataloader.loadAllMatchIds()
        all_telemetry_ids = self.dataloader.loadAllTelemetryIds()
        match_ids_without_telemetry = list(set(all_match_ids) - set(all_telemetry_ids))
        print(f'found {len(match_ids_without_telemetry)} matches without telemetry, starting download..')
        for match_id in match_ids_without_telemetry:
            #print(match_id)
            match_data = self.dataloader.loadMatchData(matchId=match_id)
            #if not self.db.telemetryExists(matchId=match['matchId']):
            print(f'downloading telemetry for: {match_id}')
            matchTelemetry = self.interwebs.webGetFullTelemetryByMatchData(match_data)
            if matchTelemetry:
                self.db.saveTelemetry(matchId=match_id, telemetry=matchTelemetry)
            #else:
                #print(f'{match["matchId"]} already exists')

class LocalDataBasePopulator:
    def __init__(self):
        self.db = DBHandle(db_host, "5432", "pubgstatz", "pubgstatz", "pubgstatz")
        
    def populateWithLocalJsons(self, relativeFolder: str):
        print('not tested yet')
        #jsonReader = JsonReader(relativeFolder)
        #telemetryJsons = jsonReader.telemetryJsons
        #for telemetry in telemetryJsons:
        #    self.db.saveTelemetry(telemetry.matchId, telemetry.json)

    def saveLocations(self, matchId: str, locations: list):
        self.db.saveLocations(matchId=matchId, locations=locations)

class DataLoader:
    def __init__(self):
        self.db = DBHandle(db_host, "5432", "pubgstatz", "pubgstatz", "pubgstatz")

    def loadLocations(self, matchId: str):
        return self.db.loadLocations(matchId=matchId)

    def loadUniquePlayers(self, count: int):
        return [x[0] for x in self.db.loadData(
            #'select': f"data -> 'data' -> 'attributes' -> 'mapName'",
            #'select': f"data",
            #'where': f"data -> 'data' -> 'attributes' ->> 'mapName' = 'Summerland_Main'"
            #'select': f"data -> 'included' -> "
            f"select distinct participant -> 'attributes' -> 'stats' ->> 'name' from (select json_array_elements(data->'included') from matches) as json_object(participant) where participant ->> 'type' = 'participant' and random() < 0.001 limit {count}"
            #f"select participant ->> 'id', participant -> 'attributes' -> 'stats' ->> 'name' from (select json_array_elements(data->'included') from matches) as json_object(participant) where participant ->> 'type' = 'participant'"
            #f"select json_array_elements(data->'included') ->> 'id' as participant from matches"
        )]

    def loadAllMatchIds(self):
        return [x[0] for x in self.db.loadData(
            "select id from matches"
        )]

    def loadAllTelemetryIds(self):
        return [x[0] for x in self.db.loadData(
            "select id from telemetries"
        )]

    def loadAllLocationIds(self):
        return[x[0] for x in self.db.loadData(
            "select id from locations"
        )]

    def loadMatchIds(self, gameMode: str, mapName: str, limit: int=None) -> list:
        query = getQueryString('allMatchIds_by_gameMode_mapName.sql')
        query = query.replace('{mapName}', mapName)
        query = query.replace('{gameMode}', gameMode)
        if limit:
            query += f'LIMIT {limit}'
        #print(query)
        #exit()
        result = [x[0] for x in self.db.loadData(query)]
        return result

    def loadMatchIdCount(self, gameMode: str, mapName: str) -> int:
        query = getQueryString('matchId_count.sql')
        query = query.replace('{mapName}', mapName)
        query = query.replace('{gameMode}', gameMode)
        result = self.db.loadData(query)[0][0]
        return result


    def loadTelemetry(self, matchId: str):
        return self.db.loadData(
            f"select data from telemetries where id='{matchId}'"
        )[0][0]

    def loadWinners(self, mapName: str, gameType: str):
        query = getQueryString('winners.sql')
        winners = [{
            'matchId': x[0],
            'playerId': x[1]
        } for x in self.db.loadData(query)]
        winners_by_matches = {}
        for winner in winners:
            if winner['matchId'] not in winners_by_matches:
                winners_by_matches[winner['matchId']] = [winner['playerId']]
            else:
                winners_by_matches[winner['matchId']].append(winner['playerId'])
        return winners_by_matches

    def loadMatchData(self, matchId: str):
        return self.db.loadData(
            f"select data from matches where id='{matchId}'"
        )[0][0]


    def loadExampleMatchData(self):
        return self.db.loadData(
            "select * from matches limit 1"
        )

    def loadAllParachuteLandings(self, mapName: str):
        query = getQueryString('parachuteLandings.sql')
        query = query.replace('{mapName}', mapName)
        result = self.db.loadData(query)
        return [{
                'matchId': x[0],
                'event': x[1]
            } for x in result
        ]


    def loadAllPlayerPositions(self, mapName: str):
        query = getQueryString('playerPositions.sql')
        query = query.replace('{mapName}', mapName)
        result = self.db.loadData(query)
        return [{
                'matchId': x[0],
                'event': x[1]
            } for x in result
        ]

    def loadAllEvents(self, mapName):
        query = getQueryString('allEvents.sql')
        result = self.db.loadData(query)
        return [{
                'matchId': x[0],
                'event': x[1]
            } for x in result
        ]

    def loadWinnersPositions(self, mapName: str, gameType: str):
        winners = self.loadWinners(mapName, gameType)
        all_positions = self.loadAllPlayerPositions(mapName) # replace with load all events
        winners_positions = []
        for position in all_positions:
            matchId = position['matchId']
            playerId = position['event']['character']['accountId']
            if matchId in winners and playerId in winners[matchId]:
                winners_positions.append(position)
        return winners_positions

    def loadAllWinningParachuteLandings(self, mapName: str):
        print('yolo')


    def loadDatabaseStatus(self):
        databaseStatus = {}
        size = self.db.loadData("SELECT pg_size_pretty( pg_database_size('pubgstatz') );")[0][0]
        print(f'database size: {size}')
        time.sleep(5)
        for gameMode in gameModes:
            databaseStatus[gameMode] = {}
            for mapName in mapNames:
                c = self.loadMatchIdCount(gameMode=gameMode, mapName=mapName)
                print(f'gameMode: {gameMode}, mapName: {mapName}: {c}')
                databaseStatus[gameMode][mapNames[mapName]] = c

        return databaseStatus


# all _T events from karakin # select json_array_elements(data) from telemetries where id in (select id from matches where data -> 'data' -> 'attributes' ->> 'mapName'='Summerland_Main')

class LocalOperations:
    def parseJumpdistanceVsRank(self, relativeFolder):
        print('lol')
from dbHandle import DBHandle, getQueryString
from interwebs import Interwebs
from fileIO import JsonReader
import json
import os
from immutables import gameModes, mapNames

class WebDataBasePopulator:
    def __init__(self):
        self.db = DBHandle("localhost", "5432", "pubgstatz", "pubgstatz", "pubgstatz")
        self.interwebs = Interwebs(token=os.environ.get('PUBG_TOKEN'))

    def saveAllMatchesOfPlayer(self, playerName):
        matchIds = self.interwebs.webGetMatchIdsOfPlayer(playerName)
        print(f'found: {len(matchIds)} matches')
        for matchId in matchIds:
            if not self.db.matchExists(matchId=matchId):
                print(f'downloading match: {matchId}')
                matchJson = self.interwebs.webGetMatchData(matchId)
                self.db.saveMatch(matchId, matchJson)
            else:
                print(f'match exists: {matchId}')


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

    def loadMatchIds(self, gameMode: str, mapName: str) -> list:
        query = getQueryString('allMatchIds_by_gameMode_mapName.sql')
        query = query.replace('{mapName}', mapName)
        query = query.replace('{gameMode}', gameMode)
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
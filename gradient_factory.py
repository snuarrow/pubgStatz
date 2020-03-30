from parseTool import TelemetryParser
from flows import DataLoader, LocalDataBasePopulator
import multiprocessing
from plotter import plotPlayerChronology
import json
from tools import DateTools
from datetime import datetime, timedelta
import numpy
import time
import gc

def chunks(l, n):
    chunks = []
    for i in range(0, n):
        chunks.append(l[i::n])
    return chunks

class GradientFactory:
    def __init__(self, width: int, height: int, gameMode: str, mapName: str):
        self.width = width
        self.height = height
        self.interval = 3
        self.dataloader = DataLoader()
        self.gameMode = gameMode
        self.mapName = mapName
        self.datetools = DateTools()
        self.intervalPositions = []

    def launch(self, threads: int=1):
        matchIds = self.dataloader.loadMatchIds(gameMode=self.gameMode, mapName=self.mapName)
        locationIds = self.dataloader.loadAllLocationIds()
        telemetryIds = self.dataloader.loadAllTelemetryIds()
        unprocessed_match_ids = list(set(matchIds).intersection(set(telemetryIds)) - set(locationIds))
        print(f'matchIds: {len(matchIds)}')
        print(f'locationIds: {len(locationIds)}')
        print(f'telemetryIds: {len(telemetryIds)}')
        print(f'unprocessed_match_ids: {len(unprocessed_match_ids)}')
        #exit()
        matchIds = [{
            'matchId': x,
            'i': i+1
        } for i, x in enumerate(unprocessed_match_ids)]
        if threads > 1:
            idChunks = chunks(matchIds ,threads)
            threadpool = []
            notary = True
            for ids in idChunks:
                thread = multiprocessing.Process(
                    target=self.append,
                    args=(ids, len(matchIds),),
                    daemon=True
                )
                notary = False
                threadpool.append(thread)
                thread.start()
            for thread in threadpool:
                thread.join()
        else:
            self.append(matchIds, len(matchIds))


    def _binarySearch(self, events: list, toBeFound: datetime, left: int = 0, right: int = None):
        if not right:
            right = len(events) - 1
        mid = round((left + right) / 2)
        if left == mid or right == mid:
            leftDist = abs(toBeFound - self.datetools.toDateTime_ms_accuracy(events[left]))
            rightDist = abs(toBeFound - self.datetools.toDateTime_ms_accuracy(events[right]))
            if leftDist < rightDist:
                return left, left
            return right, left
        subtraction = self.datetools.toDateTime_ms_accuracy(events[mid]) - toBeFound
        if subtraction >= timedelta(0):
            return self._binarySearch(events, toBeFound, left, mid)
        else:
            return self._binarySearch(events, toBeFound, mid, right)

    def _playerIntervals(self, intervals: list, playerChronology: list, rank: int, teamId: int):
        out = []
        left = 0
        playerEventTimes = [x['_D'] for x in playerChronology]
        previousEventTime = None
        for i, interval in enumerate(intervals):
            index, left = self._binarySearch(events=playerEventTimes, toBeFound=interval, left=left)
            eventTime = playerChronology[index]['_D']
            if not previousEventTime or eventTime == previousEventTime:
                previousEventTime = eventTime
                out.append(None)
                continue
            previousEventTime = eventTime
            out.append({
                'location': playerChronology[index]['character']['location'],
                'rank': rank,
                'teamId': teamId,
            })
        return out

    def _cutTail(self, playerIntervals: list):
        def getLastPositionIndex(playerIntervals: list):
            playerIntervals.reverse()
            for i, p in enumerate(playerIntervals):
                if p:
                    playerIntervals.reverse()
                    return len(playerIntervals) - i
            playerIntervals.reverse()
            return 0

        i = getLastPositionIndex(playerIntervals)
        return playerIntervals[:i]

    def _interpolatePlayerIntervals(self, playerIntervals: list):
        previousP = playerIntervals[0]
        for i, p in enumerate(playerIntervals):
            if not p:
                playerIntervals[i] = previousP
            previousP = p
        return playerIntervals

    def append(self, matchIds: list, totalMatchIds: int):
        localDataBasePopulator = LocalDataBasePopulator()
        dataloader = DataLoader()
        for matchId in matchIds:
            print(f'matchId: {matchId["i"]} / matchIds: {totalMatchIds}')
            try:
                telemetry = dataloader.loadTelemetry(matchId=matchId['matchId'])
            except IndexError:
                print(f'gradient_factory telemetry load error: {matchId}')
                continue
            telemetryParser = TelemetryParser(telemetry)
            playerChronologies = telemetryParser.parsePlayerChronologies()
            matchStart = telemetryParser.matchStart()
            matchEnd = telemetryParser.matchEnd()
            matchLocations = []
            intervals = self.datetools.getIntervals(startTime=matchStart, endTime=matchEnd, intervalSeconds=self.interval)
            for accountId in playerChronologies:
                #plotPlayerChronology(playerChronology=playerChronologies[accountId], matchStart=matchStart, matchEnd=matchEnd)
                try:
                    teamData = telemetryParser.teamIds[accountId]
                except KeyError:
                    continue
                playerChronology = playerChronologies[accountId]
                playerIntervals = self._playerIntervals(intervals=intervals, playerChronology=playerChronology, rank=teamData['rank'], teamId=teamData['teamId'])
                #print(json.dumps(playerIntervals, indent=4))
                #exit()
                playerIntervals = self._cutTail(playerIntervals=playerIntervals)
                playerIntervals = self._interpolatePlayerIntervals(playerIntervals=playerIntervals)
                for i, p in enumerate(playerIntervals):
                    if i == len(matchLocations):
                        matchLocations.append([])
                    matchLocations[i].append(p)
            
            locations = []
            for i, locationInterval in enumerate(matchLocations):
                elapsedTime = i * self.interval
                out = {
                    'elapsedTime': elapsedTime,
                    'locations': locationInterval
                }
                
                locations.append(out)
                #print(f'{i} {len(locationInterval)}')
                #print(matchId['matchId'])
                #print(json.dumps(out, indent=4))
                #exit()
            #print(json.dumps(locations[2], indent=4))
            #exit()
            #print(len(locations))
            localDataBasePopulator.saveLocations(matchId=matchId['matchId'], locations=locations)
            #l = dataloader.loadLocations(matchId=matchId['matchId'])
            #print(len(l))

            del locations
            del telemetry
            del playerChronologies
            del intervals
            del telemetryParser
            #print(gc.collect())


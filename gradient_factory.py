from parseTool import TelemetryParser
from flows import DataLoader
import threading
from plotter import plotPlayerChronology
import json
from tools import DateTools

def chunks(l: list, n: int):
    n = max(1, n)
    return [l[i:i+n] for i in range(0, len(l), n)]

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

    def launch(self, threads: int):
        matchIds = self.dataloader.loadMatchIds(gameMode=self.gameMode, mapName=self.mapName)[:1]
        if threads > 1:
            idChunks = chunks(matchIds, threads)
            for i, idChunk in enumerate(idChunks):
                threadPool = []
                print(f'processing chunk {i}/{len(idChunks)}')
                for matchId in idChunk:
                    thread = threading.Thread(target=self.append, args=(matchId,))
                    thread.start()
                    threadPool.append(thread)
                for thread in threadPool:
                    thread.join()
        else:
            for matchId in matchIds:
                self.append(matchId)

    #def _getIntervals(self, matchStartTime: datetime, matchEndTime: datetime):
    ##    intervals = []
    #    current = matchStartTime
    #    while current < matchEndTime:
    #        current += 

    def append(self, matchId: str):
        telemetry = self.dataloader.loadTelemetry(matchId=matchId)
        self.telemetryParser = TelemetryParser(telemetry)
        playerChronologies = self.telemetryParser.parsePlayerChronologies()
        matchStart = self.telemetryParser.matchStart()
        matchEnd = self.telemetryParser.matchEnd()
        intervals = self.datetools.getIntervals(startTime=matchStart, endTime=matchEnd, intervalSeconds=self.interval)
        for accountId in playerChronologies:
            
            #plotPlayerChronology(playerChronology=playerChronologies[accountId], matchStart=matchStart, matchEnd=matchEnd)
            exit()

    #def append(self, telemetry: list):
        

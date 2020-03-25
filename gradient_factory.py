from parseTool import TelemetryParser
from flows import DataLoader
import threading
from plotter import plotPlayerChronology
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

    def _binary_search(self, events: list, toBeFound: datetime, left: int, right: int, previous_distance: timedelta, previous_mid: int):
        mid = round((left + right) / 2)
        subtraction = self.datetools.toDateTime_ms_accuracy(events[mid]['_D']) - toBeFound
        if abs(subtraction) > previous_distance:
            return events[previous_mid]
        if left == mid or right == mid:
            return events[mid]
        if subtraction >= timedelta(0):
            return binarySearch(events, toBeFound, left, mid, abs(subtraction), mid)
        else:
            return binarySearch(events, toBeFound, mid, right, abs(subtraction), mid)

    def append(self, matchId: str):
        telemetry = self.dataloader.loadTelemetry(matchId=matchId)
        self.telemetryParser = TelemetryParser(telemetry)
        intervals = self.datetools.getIntervals(self.telemetryParser.)
        playerChronologies = self.telemetryParser.parsePlayerChronologies()
        for accountId in playerChronologies:
            #plotPlayerChronology(playerChronologies[accountId])
            exit()






def make_frames(grouped_events: dict, interval_seconds: int):
    def binarySearch(datetools: DateTools, events: list, toBeFound: datetime, left: int, right: int, previous_distance: timedelta):
        mid = round((left + right) /  2)
        #print(type(events))
        #print(f'left: {left}, right: {right}, mid: {mid}, len events: {len(events)}')
        subtraction = datetools.toDateTime_ms_accuracy(events[mid]['_D']) - toBeFound
        current_distance = abs(subtraction)
        if left == mid or right == mid:
            return events[mid]  
        if subtraction >= timedelta(0):
            return binarySearch(datetools, events, toBeFound, left, mid, abs(subtraction))
        else:
            return binarySearch(datetools, events, toBeFound, mid, right, abs(subtraction))

    num_frames = 0
    datetools = DateTools()
    frames = []
    for k, matchId in enumerate(grouped_events):
        print(f'generate frames: {k+1}/{len(grouped_events)}, num frames: {num_frames}')
        #print(json.dumps(grouped_events[matchId]['account.ccc4fc71e5274a32ac4bb89c2439e4ad'], indent=4))
        #exit()
        first_datetime = datetools.toDateTime_ms_accuracy(grouped_events[matchId]['first']['_D'])
        last_datetime = datetools.toDateTime_ms_accuracy(grouped_events[matchId]['last']['_D'])
        intervals = datetools.getIntervals(first_datetime, last_datetime, interval_seconds)
        for accountId in grouped_events[matchId]:
            if accountId not in ['first', 'last']:
                playerEvents = grouped_events[matchId][accountId]
                #print(json.dumps(playerEvents, indent=4))
                #exit()
                for i, interval in enumerate(intervals):
                    eventAtInterval = binarySearch(datetools=datetools, events=playerEvents, toBeFound=interval, left=0, right=len(playerEvents)-1, previous_distance=timedelta(days=1))
                    try:
                        frames[i].append(eventAtInterval)
                    except IndexError:
                        frames.append([])
                        frames[i].append(eventAtInterval)
                    if i > num_frames:
                        num_frames = i
    return frames
        

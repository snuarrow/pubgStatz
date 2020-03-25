import datetime
from datetime import datetime, timedelta

def ifEvent(elem):
    if isinstance(elem, dict):
        return elem["_D"]
    return elem

class DateTools:
    def getIntervals(self, startTime: datetime, endTime: datetime, intervalSeconds: int):
        startTime = ifEvent(startTime)
        endTime = ifEvent(endTime)
        td = timedelta(seconds=intervalSeconds)
        currentTime = startTime
        return_list = []
        return_list.append(currentTime)
        while currentTime < endTime:
            currentTime += td
            return_list.append(currentTime)

        return return_list

    def toDateTime_ms_accuracy(self, pubgTimeStamp):
        return datetime.strptime(pubgTimeStamp, '%Y-%m-%dT%H:%M:%S.%fZ')

    def toDateTime_s_accuracy(self, pubgTimeStamp):
        return datetime.strptime(pubgTimeStamp, '%Y-%m-%dT%H:%M:%SZ')

    def elapsedTime(self, timeStamp0, timeStamp1):
        print("Error: not implemented yet.")

    def inRange(self, startTime: datetime, current: datetime, endTime: datetime):
        return current >= startTime and current <= endTime

class LocationTools:
    def dist(self, pointA, pointB):
        print("Error: not implemented yet")
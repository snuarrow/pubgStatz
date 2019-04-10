import datetime

class DateTools:
    def toDateTime_ms_accuracy(self, pubgTimeStamp):
        return datetime.datetime.strptime(pubgTimeStamp, '%Y-%m-%dT%H:%M:%S.%fZ')

    def toDateTime_s_accuracy(self, pubgTimeStamp):
        return datetime.datetime.strptime(pubgTimeStamp, '%Y-%m-%dT%H:%M:%SZ')

    def elapsedTime(self, timeStamp0, timeStamp1):
        print("Error: not implemented yet.")
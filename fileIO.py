import os
import json
from objects import TelemetryJson

class JsonReader:
    def __init__(self, relativeFolder):
        print('JsonReader initialized')
        self.relativeFolder = relativeFolder
        self.telemetryJsons = self.__loadProcessableTelemetries()

    def __loadListOfProcessableFiles(self, relativeFolder):
        return list(
            map(
                lambda f: os.path.join(relativeFolder, str(f)),
                filter(
                    lambda file: '.json' in str(file),
                    os.listdir(relativeFolder)
                )
            )
        )

    def __loadProcessableTelemetries(self):
        return list(
            map(
                lambda filename: TelemetryJson(filename.rstrip('-telemetry'), json.load(open(filename, 'r'))),
                self.__loadListOfProcessableFiles(self.relativeFolder)  
            )
        )

if __name__ == "__main__":
    jsonReader = JsonReader('json')

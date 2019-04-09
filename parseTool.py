from objects import Contender

class ParseTool:
    def getUrlFromMatchData(self, matchData):
        for it in matchData["included"]:
            if 'URL' in it["attributes"]:
                return it["attributes"]["URL"]
        return "de nada"

    def parseContedersFromMatchData(self, matchData):
        contenders = dict()
        for it in matchData["included"]:
            if 'type' in it and it["type"] == "participant":
                contenders[it["attributes"]["stats"]["name"]] = Contender(
                    it["id"],
                    it["attributes"]["stats"]["name"],
                    it["attributes"]["stats"]["winPlace"]
                )
        return contenders

    def filterMatchDataByGameMode(self, gameMode, matchDatas):
        return list(filter(lambda x: x["data"]["attributes"]["gameMode"] == gameMode, matchDatas))

    def crawlLandingTimes(self, telemetryData):
        landingTimes = dict()
        for it in telemetryData:
            if '_T' in it:
                if it["_T"] == "LogParachuteLanding":
                    name = it["character"]["name"]
                    landingTime = it["_D"]
                    landingTimes[name] = landingTime
        return landingTimes

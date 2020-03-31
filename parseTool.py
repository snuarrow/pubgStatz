from objects import Contender, Location

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

class TelemetryParser:
    def __init__(self, telemetryJson):
        print('TelemetryParser initialized')
        self.contenders = dict()
        self.matchData = dict()
        self.firstJumpLocation =  None
        self.firstLandTime =  None
        self.lastJumpLocation = None
        self.isFirstLand = True
        self.isFirstJump = True
        self.parseTValues(telemetryJson)

    def parseTValues(self, telemetryJson):
        if len(telemetryJson) < 300:
            print('Error: invalid telemetryJson, should be longer than 300 lines, exit(78)')
            exit(78)
        for item in telemetryJson:
            if '_T' in item:
                t = item['_T']
                if t == 'LogMatchEnd':
                    self.parseLogMatchEnd(item)
                elif t == "LogParachuteLanding":
                    self.parseLogParachuteLanding(item)
                elif t == "LogVehicleLeave":
                    self.parseLogVehicleLeave(item)

    def parseLocation(self, t):
        accountId = t['character']['accountId']
        x = t["character"]['location']['x']
        y = t["character"]['location']['y']
        z = t["character"]['location']['z']
        timeStamp = t["_D"]
        return accountId, Location(x,y,z), timeStamp

    def parseLogMatchEnd(self, matchEndT):
        for player in matchEndT["characters"]:
            if 'name' in player:
                name = player["name"]
                rank = player["ranking"]
                accountId = player["accountId"]
                if self.contenders[accountId] == None:
                    self.contenders[accountId] = Contender()
                contender = self.contenders[accountId]
                contender.accountId = accountId
                contender.rank = rank
                contender.name = name
                self.contenders[accountId] = contender

    def parseLogParachuteLanding(self, parachuteLandingT):
        accountId,location, timeStamp = self.parseLocation(parachuteLandingT)
        self.contenders[accountId].landingLocation = location
        self.contenders[accountId].landingTime = timeStamp

        if self.isFirstLand == True:
            self.firstLandTime = timeStamp
            self.isFirstLand = False

    def parseLogVehicleLeave(self, logVehicleLeaveT):
        if logVehicleLeaveT["vehicle"]["vehicleType"] == 'TransportAircraft':
            self.parseJumpStart(logVehicleLeaveT)

    def parseJumpStart(self, logJumpStartT):
        accountId,location,timeStamp = self.parseLocation(logJumpStartT)
        contender = None

        try:
            contender = self.contenders[accountId]
        except:
            contender = Contender()
            
        contender.accountId = accountId
        contender.jumpLocation = location
        contender.jumpTime = timeStamp
        self.contenders[accountId] = contender

        if self.isFirstJump == True:
            self.firstJumpLocation = location
            self.isFirstJump = False
        else:
            self.lastJumpLocation = location



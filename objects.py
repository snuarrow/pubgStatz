class Contender:
    landingLocation = None
    jumpLocation = None
    accountId = None
    name = None
    rank = None
    jumpTime = None
    landingTime = None
    distanceFromFlightPath = None
    landingTimeDelta = None
    jumpDistance = None

class Location:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def distanceFromFlightPath(self, firstJumpLocation, lastJumpLocation):
        return abs((lastJumpLocation.y-firstJumpLocation.x)*(firstJumpLocation.y-self.y) - (firstJumpLocation.x-self.x)*(lastJumpLocation.y-firstJumpLocation.y)) / np.sqrt(np.square(lastJumpLocation.x-firstJumpLocation.x) + np.square(lastJumpLocation.y-firstJumpLocation.y))

class Match:
    firstCirclePosition = None

class TelemetryJson:
    def __init__(self, matchId, json):
        self.matchId = matchId
        self.json = json

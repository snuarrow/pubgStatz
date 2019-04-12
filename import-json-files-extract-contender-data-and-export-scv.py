import os
import shutil
import json

class Contender:
  landingLocation = None
  jumpLocation = None
  accountId = None
  name = None
  rank = None
  jumpTime = None
  landingTime = None
  distanceFromFlightPath = None

class Location:
    def __init__(self, x, y, z):
      self.x = x
      self.y = y
      self.z = z

    def distanceFromFlightPath(self, firstJumpLocation, lastJumpLocation):
      return abs((jumpX-startX)*(firstJumpLocation.y-self.y) - (firstJumpLocation.x-self.x)*(lastJumpLocation.y-firstJumpLocation.y)) / np.sqrt(np.square(lastJumpLocation.x-firstJumpLocation.x) + np.square(lastJumpLocation.y-firstJumpLocation.y))


class TelemetryParser:
  def __init__(self, telemetryJson):
    self.contenders = dict()
    self.firstJumpLocation =  None
    self.lastJumpLocation = None
    self.isFirstJump = True
    self.zoidberg(telemetryJson)


  def zoidberg(self, telemetryJson):
    print("QQQQQQQQQ: "+str(len(telemetryJson)))
    if len(telemetryJson) < 300:
      return
    for item in telemetryJson:
      if '_T' in item:
        t = item['_T']

        if t == 'LogMatchEnd':
          self.parseLogMatchEnd(item)

        elif t == "LogParachuteLanding":
          self.parseLogParachuteLanding(item)

        elif t == "LogVehicleLeave":
          self.parseLogVehicleLeave(item)

      #elif t == "LogGameStatePeriodic" and item['common']['isGame'] == 1.5:


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
          self.contenders[accountId].rank = rank
          self.contenders[accountId].name = name
          self.contenders[accountId].accountId = accountId

  def parseLogParachuteLanding(self, parachuteLandingT):
    accountId,location, timeStamp = self.parseLocation(parachuteLandingT)
    self.contenders[accountId].landingLocation = location
    self.contenders[accountId].landingTime = timeStamp


  def parseLogVehicleLeave(self, logVehicleLeaveT):
    #print(".......: "+logVehicleLeaveT["vehicle"])
    if logVehicleLeaveT["vehicle"]["vehicleType"] == 'TransportAircraft':
      self.parseJumpStart(logVehicleLeaveT)

  def parseJumpStart(self, logJumpStartT):
    accountId,location,timeStamp = self.parseLocation(logJumpStartT)
    try:
      self.contenders[accountId]
    except:
      self.contenders[accountId] = Contender()


    self.contenders[accountId].jumpLocation = location
    self.contenders[accountId].jumpTime = timeStamp
    if self.isFirstJump == True:
      self.firstJumpLocation = location
      self.isFirstJump = False
    else:
      self.lastJumpLocation = location

asd = []

cwd = os.getcwd() #current dir
processable_files = list(map(lambda f: str(f), (filter(lambda file: '.json' in str(file), os.listdir("json/")))))
for filename in processable_files:
    try:
      input_file=open('json/'+filename, 'r')
      telemetryFile=json.load(input_file)
      tp = TelemetryParser(telemetryFile)
      print("contenders: "+str(len(tp.contenders)))
      for contender in tp.contenders:
        print(contender.accountId)
        try:
          #contender.distanceFromFlightPath = contender.landingLocation.distanceFromFlightPath(tp.firstJumpLocation, tp.lastJumpLocation)
          #asd.append((contender.distanceFromFlightPath, contender.rank))
          asd.append((0,contender.rank))
        except:
          continue

    except (IOError,ValueError, filename == 'land-location-data.json'):
      print ('error: '+str(IOError))

print("dist,rank"+str(len(asd)))
for lol in asd:
  print(str(lol[0])+","+str(lol[1]))


















'''
cwd = os.getcwd() #current dir
output_file=open('land-location-data.json', 'w')
result = []

for filename in os.listdir(cwd):
    try:
        input_file=open(filename, 'r')
        telemetryFile=json.load(input_file)

#        print "ranking, distance"

        for item in telemetryFile:
            rankki={}
            parachute={}

            if '_T' in item:

                #loyda pelaajan lopullinen rankki
                if item["_T"] == "LogMatchEnd":
                    for player in item["characters"]:
                        if 'name' in player:
                            rankki = player["ranking"]
                            name = player["name"]
 #                           print str(name)+", "+str(rankki)
                            rankki=player["ranking"]
                            result.append(rankki)
#                    print "match break"


                #loyda player landlocation
                elif item["_T"] == "LogParachuteLanding":
                    for player in item["character"]:
                        if 'location' in player:
                            name = item['character']['name']
                            x = item["character"]['location']['x']
                            y = item["character"]['location']['y']
                            z = item["character"]['location']['z']
                            parachute=str(x)+":"+str(y)
                            result.append(parachute)
                            #print name+", "+str(x)
                            print str(name)+', '+str(x)+', '+str(y)


                #loyda player aircraft leave location
                elif  item["_T"] == "LogVehicleLeave":
                  if item['vehicle']['vehicleType'] == 'TransportAircraft':
                    for player in item["character"]:
                        if 'location' in player:
                            name = item['character']['name']
                            x = item["character"]['location']['x']
                            y = item["character"]['location']['y']
                            z = item["character"]['location']['z']
                            parachute=str(x)+":"+str(y)
                            result.append(parachute)
                            #print name+", "+str(x)
#                            print str(x)+', '+str(y)


                #loyda safezonelocation pelin hetkella 1.5
                elif (item["_T"] == "LogGameStatePeriodic" and item['common']['isGame'] == 1.5):
                    safezoneX = item['gameState']['poisonGasWarningPosition']['x']
                    safezoneY = item['gameState']['poisonGasWarningPosition']['y']
#                    print 'Circleposition, '+str(safezoneX)+', '+str(safezoneY)
                    #break #tata ei taida tarvita

    except (IOError,ValueError, filename == 'land-location-data.json'):
        pass

json.dump(result, output_file)

'''

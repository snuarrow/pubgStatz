import os
import shutil
import json
import math
import numpy as np
import csv
import datetime
import dateutil.parser as dp

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
  killCount = 0

class Match:
  firstCirclePosition = None

class Location:
    def __init__(self, x, y, z):
      self.x = x
      self.y = y
      self.z = z

    def distanceFromFlightPath(self, firstJumpLocation, lastJumpLocation):
      return abs((lastJumpLocation.y-firstJumpLocation.x)*(firstJumpLocation.y-self.y) - (firstJumpLocation.x-self.x)*(lastJumpLocation.y-firstJumpLocation.y)) / np.sqrt(np.square(lastJumpLocation.x-firstJumpLocation.x) + np.square(lastJumpLocation.y-firstJumpLocation.y))


class TelemetryParser:
  def __init__(self, telemetryJson):
    self.contenders = dict()
    self.matchData = dict()
    self.firstJumpLocation =  None
    self.firstLandTime =  None
    self.lastJumpLocation = None
    self.isFirstLand = True
    self.isFirstJump = True
    self.parseTValues(telemetryJson)


  def parseTValues(self, telemetryJson):
    #print("QQQQQQQQQ: "+str(len(telemetryJson)))
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

        elif t == "LogPlayerKill":
          self.parseLogPlayerKillStats(item)

        '''
        elif t == "LogGameStatePeriodic" and item['common']['isGame'] == 1.5:
          self.parseGameState(item)
        '''
  '''
  def parseGameState(self,t):
    match = None
    safezoneX = t['gameState']['poisonGasWarningPosition']['x']
    safezoneY = t['gameState']['poisonGasWarningPosition']['y']

    try:
      match = self.matchData[matchId]
    except:
      match = matchData()
      match.matchId = matchId
      match.SafezoneLocationGameState1 = location
      
      self.matchData[matchId] = match
    return 'tuut'
  '''

  def parseLogPlayerKillStats(self, LogPlayerKillT):
    for player in LogPlayerKillT["victimGameResult"]:      
      accountId = LogPlayerKillT["victimGameResult"]["accountId"]
      killCount = LogPlayerKillT["victimGameResult"]["stats"]["killCount"]
      distanceOnFoot = LogPlayerKillT["victimGameResult"]["stats"]["distanceOnFoot"]
      distanceOnVehicle = LogPlayerKillT["victimGameResult"]["stats"]["distanceOnVehicle"]
      distanceOnParachute = LogPlayerKillT["victimGameResult"]["stats"]["distanceOnParachute"]
      distanceOnFreefall = LogPlayerKillT["victimGameResult"]["stats"]["distanceOnFreefall"]
      contender = self.contenders[accountId]
      contender.accountId = accountId
      contender.killCount = killCount
      contender.distanceOnFoot =  int(round(distanceOnFoot))
      contender.distanceOnVehicle = int(round(distanceOnVehicle))
      contender.distanceOnParachute = int(round(distanceOnParachute))
      contender.distanceOnFreefall = int(round(distanceOnFreefall))
      self.contenders[accountId] = contender

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
            print ''
          else:
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
    #print(".......: "+logVehicleLeaveT["vehicle"])
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



def landingTimeDelta(landingTime, firstLandTime):

    startTime = datetime.datetime.strptime(firstLandTime, '%Y-%m-%dT%H:%M:%S.%fZ')
    endTime = datetime.datetime.strptime(landingTime, '%Y-%m-%dT%H:%M:%S.%fZ')

    timeDifference = endTime - startTime
    d = str(timeDifference)
    parsedTime = dp.parse(d)
    S = int(parsedTime.strftime('%S'))
    M = int(parsedTime.strftime('%M'))
    f = int(parsedTime.strftime('%f'))

    timeDifferenceInSeconds = datetime.timedelta(seconds=M*60+S+float(f)/1000000).total_seconds()

    return timeDifferenceInSeconds

parsedContendersData = []

cwd = os.getcwd() #current dir
processable_files = list(map(lambda f: str(f), (filter(lambda file: '.json' in str(file), os.listdir("json/")))))
for filename in processable_files:
    try:
      input_file=open('json/'+filename, 'r')
      telemetryFile=json.load(input_file)
      tp = TelemetryParser(telemetryFile)
      #print("contendersamount: "+str(len(tp.contenders))) #printtaa contender listan pituus
      #print filename
      for accountId in tp.contenders:
        contender = tp.contenders[accountId]

        try:
          contender.distanceFromFlightPath = int(round(contender.landingLocation.distanceFromFlightPath(tp.firstJumpLocation, tp.lastJumpLocation)))
          contender.landingTimeDelta = int(round(landingTimeDelta(contender.landingTime, tp.firstLandTime)))
          contender.jumpDistance = int(round(math.sqrt( (contender.landingLocation.x - contender.jumpLocation.x)**2 + (contender.landingLocation.y - contender.jumpLocation.y)**2 )))

          parsedContendersData.append((contender.distanceFromFlightPath, contender.rank, contender.landingTimeDelta, contender.jumpDistance, contender.killCount, contender.distanceOnVehicle,  contender.distanceOnParachute,  contender.distanceOnFreefall, contender.distanceOnFoot)) #koosta lista halutuista tiedoista
        except:
          continue

    except (IOError,ValueError, filename == 'land-location-data.json'):
      print ('error: '+str(IOError))

#print str(len(parsedContendersData)) ##printtaa listan pituus



#tama toimii!
print("distance,rank,landtimeDelta,jumpDistance,distanceOnFoot") #printtaa listan otsikko niista mista haluat
for parsedContender in parsedContendersData:
  print(str(parsedContender[0])+","+str(parsedContender[1])+","+str(parsedContender[2])+","+str(parsedContender[3])+","+str(parsedContender[4])+","+str(parsedContender[5])+","+str(parsedContender[6])+","+str(parsedContender[7])+","+str(parsedContender[8])) #printtaa halutut tiedot




#csv save toimii
'''
with open('employee_file2.csv', mode='wb') as csv_file:
  fieldnames = ['distance', 'rank', 'landingTime']
  writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
  writer.writeheader()
  for parsedContender in parsedContendersData:
      writer.writerow({'distance':(str(parsedContender[0])),'rank':(str(parsedContender[1])),'landingTime':(str(parsedContender[2]))})
'''













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

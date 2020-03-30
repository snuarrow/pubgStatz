import requests
from parseTool import ParseTool
import json
import datetime
import time
import urllib3

class Interwebs:

    parseTool = ParseTool()

    def __init__(self, token: str):
        if not token:
            print('PUBG_TOKEN env variable not specified')
            exit(1)
        self.header = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.api+json"
        }

    def webGetMatchData(self, matchId):
        url = "https://api.pubg.com/shards/pc-eu/matches/"+matchId
        while (True):
            try:
                response = requests.get(url, headers=self.header)
            except requests.exceptions.ConnectionError as e:
                print(e)
                print(f'request connection error: {url}')
                break
            if response.status_code == 429:
                print(f'too many requests, waiting...')
                time.sleep(60)
            else:
                break

        try:
            return response.json()
        except json.decoder.JSONDecodeError as e:
            print(e)
            return None
        #return requests.get(url, headers=self.header).json()

    def webGetMatchIdsOfPlayer(self, playerName):
        url = "https://api.pubg.com/shards/steam/players?filter[playerNames]="+playerName
        #r = requests.get(url, headers=self.header).json()
        
        while(True):
            response = requests.get(url, headers=self.header)
            if response.status_code == 429:
                print(f'too many requests, waiting...')
                time.sleep(60)
            else:
                break
        try:
            r = response.json()
            return list(map(lambda x: x["id"], r["data"][0]["relationships"]["matches"]["data"]))
        except (json.decoder.JSONDecodeError, KeyError):
            print(response)
            print(response.status_code)
            return []

    def webGetFullTelemetryByMatchData(self, matchData):
        url = self.parseTool.getUrlFromMatchData(matchData)
        response = None
        try:
            response = requests.get(url)
        except (requests.exceptions.ConnectionError, urllib3.exceptions.ProtocolError, requests.exceptions.ChunkedEncodingError) as e:
            print(e)
            print(f'Error at interwebs.webGetFullTelemetryByMatchData, url: {url}')
        if response:
            try:
                return response.json()
            except json.decoder.JSONDecodeError:
                pass
        return None

    def webGetMatchesByMap(self, mapName, matchIds):
        return list(
            filter(
                lambda x: x["data"]["attributes"]["mapName"] == mapName,
                list(
                    map(lambda x: self.webGetMatchData(x), matchIds)
                )
            )
        )

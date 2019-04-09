from dbHandle import DBHandle
from interwebs import Interwebs

class WebDataBasePopulator:
    def __init__(self):
        self.db = DBHandle("localhost", "5432", "pubgstatz", "pubgstatz", "pubgstatz")
        self.interwebs = Interwebs("Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI0YTM4OGMzMC0zMmEwLTAxMzctNDIwZS0wMDU3NDUzNGQzNjMiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTUzNjc4Nzc0LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6Ii1hMjUwZjI0MS1hNGQ2LTRjZDgtOTE3NS04MGY3NGEyY2U3M2YifQ.tAMnseoVOXvOmzvUejT_cnScFC0PyaAPwZL1u4KBrUE")

    def saveAllMatchesOfPlayer(self, playerName):
        matchIds = self.interwebs.webGetMatchIdsOfPlayer(playerName)
        for matchId in matchIds:
            matchJson = self.interwebs.webGetMatchData(matchId)
            self.db.saveMatch(matchId, matchJson)
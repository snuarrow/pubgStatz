import psycopg2
import pandas as pd
import json

def getQueryString(filename: str) -> str:
    fd = open(f'sqlQueries/{filename}', 'r')
    sqlFile = fd.read()
    fd.close()
    return sqlFile

class DBHandle:
    def __init__(self, host, port, dbname, user, password):
        self.connection = self.getDBConnection(host, port, dbname, user, password)
        self.initDB()
    
    def getDBConnection(self, host, port, dbname, user, password):
        return psycopg2.connect("host="+host+" port="+port+" dbname="+dbname+ " user="+user+" password="+password)

    def getCursor(self):
        return self.connection.cursor()

    def query(self, queryString):
        return pd.read_sql(queryString, self.connection)

    def sqlCommand(self, command):
        try:
            self.getCursor().execute(command)
            self.connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: ", error)

    def initDB(self):
        self.sqlCommand("CREATE TABLE IF NOT EXISTS users (id VARCHAR NOT NULL PRIMARY KEY, data json NOT NULL)")
        self.sqlCommand("CREATE TABLE IF NOT EXISTS matches (id VARCHAR NOT NULL PRIMARY KEY, data json NOT NULL)")
        self.sqlCommand("CREATE TABLE IF NOT EXISTS telemetries (id VARCHAR NOT NULL PRIMARY KEY, data json NOT NULL)")
        self.sqlCommand("CREATE TABLE IF NOT EXISTS matchesByMap (id VARCHAR NOT NULL PRIMARY KEY, data VARCHAR NOT NULL)")

    # TODO: get rid of copypaste in save functions
    def saveUserJson(self, userId, userJson):
        try:
            if not self.loadUserJson(userId):
                self.getCursor().execute("INSERT INTO users VALUES("+str(userId)+",'"+userJson+"')")
                self.connection.commit()
            else:
                print("Error: user already exists")
        except (Exception, psycopg2.Error) as error:
            print("Failed to save user: ", error)

    # TODO: get rid of copypaste in load functions
    def loadUserJson(self, userId):
        cursor = self.getCursor()
        cursor.execute("SELECT * FROM users WHERE id="+str(userId))
        record = cursor.fetchall()
        if len(record) is 1:
            return True, record[0][1]
        else:
            return False

    def matchExists(self, matchId):
        cursor = self.getCursor()
        cursor.execute(f"select id from matches where id='{matchId}'")
        record = cursor.fetchall()
        return len(record) > 0

    # TODO: get rid of copypaste in load functions
    def loadMatchJson(self, matchId):
        cursor = self.getCursor()
        cursor.execute(f"select * from matches where id='{matchId}'")
        record = cursor.fetchall()
        if len(record) is 1:
            return True, record[0][1]
        else:
            return False

    def telemetryExists(self, matchId):
        cursor = self.getCursor()
        cursor.execute(f"select id from telemetries where id='{matchId}'")
        record = cursor.fetchall()
        return len(record) > 0

    # TODO: get rid of copypaste in load functions
    def loadTelemetryJson(self, matchId):
        cursor = self.getCursor()
        cursor.execute(f"select * from telemetries where id='{matchId}'")
        record = cursor.fetchall()

        if len(record) is 1:
            return True, record[0][1]
        else:
            return False

    # TODO: get rid of copypaste in save functions
    def saveMatch(self, matchId, matchJson):
        try:
            if not self.loadMatchJson(matchId):
                self.getCursor().execute(f"INSERT INTO matches (id, data) VALUES ('{matchId}', '{json.dumps(matchJson)}')")
                self.connection.commit()
            else:
                print("Error: match already exists")
        except (Exception, psycopg2.Error) as error:
            print(f"Failed to save match: {matchId}", error)

    # TODO: get rid of copypaste in save functions
    def saveTelemetry(self, matchId, telemetry):
        try:
            if not self.loadTelemetryJson(matchId):
                self.getCursor().execute(f"INSERT INTO telemetries (id, data) VALUES ('{matchId}', '{json.dumps(telemetry)}')")
                self.connection.commit()
            else:
                print("Error: telemetry already exists")
        except (Exception, psycopg2.Error) as error:
            print("Failed to save telemetry: ", error)

    def loadData(self, query: str):
        cursor = self.getCursor()
        cursor.execute(query)
        record = cursor.fetchall()
        return record
        #print(json.dumps(record, indent=4, default=str))
        #print(len(record))
        #exit(1)


    def loadAllMatches(self):
        cursor = self.getCursor()
        cursor.execute(f"select * from matches")
        record = cursor.fetchall()
        if len(record) > 0:
            return True, [{
                    'matchId': x[0],
                    'matchData': x[1]
                } for x in record
            ]
        else:
            return False, None

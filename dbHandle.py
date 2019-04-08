import psycopg2
import pandas as pd

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
        self.sqlCommand("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, json VARCHAR NOT NULL)")
        self.sqlCommand("CREATE TABLE IF NOT EXISTS matches (id SERIAL PRIMARY KEY, mode VARCHAR NOT NULL, map VARCHAR NOT NULL, json VARCHAR NOT NULL)")
        self.sqlCommand("CREATE TABLE IF NOT EXISTS telemetries (id SERIAL PRIMARY KEY, json VARCHAR NOT NULL)")

    def saveUserJson(self, connection, userId, userJson):
        try:
            if not self.loadUserJson(connection, userId):
                self.getCursor().execute("INSERT INTO users VALUES("+str(userId)+",'"+userJson+"')")
                connection.commit()
            else:
                print("Error: user already exists")
        except (Exception, psycopg2.Error) as error:
            print("Failed to save user: ", error)

    def loadUserJson(self, connection, userId):
        cursor = self.getCursor()
        cursor.execute("SELECT * FROM users WHERE id="+str(userId))
        record = cursor.fetchall()
        if len(record) is 1:
            return True, record[0][1]
        else:
            return False

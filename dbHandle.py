import psycopg2
import pandas as pd

conn_string = "host=localhost port=5432 dbname=pubgstatz user=pubgstatz password=pubgstatz"

#conn = psycopg2.connect(conn_string)

sql_command = "SELECT * FROM test"

#data = pd.read_sql(sql_command, conn)

#print(data.shape)

def getDBConnection(host, port, dbname, user, password):
    return psycopg2.connect("host="+host+" port="+port+" dbname="+dbname+ " user="+user+" password="+password)

def getCursor(connection):
    return connection.cursor()

def query(connection, queryString):
    return pd.read_sql(queryString, connection)

def sqlCommand(connection, command):
    try:
        getCursor(connection).execute(sql_command)
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: ", error)

def initDB(connection):
    sqlCommand(connection, "CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, json VARCHAR NOT NULL)")
    sqlCommand(connection, "CREATE TABLE IF NOT EXISTS matches (id SERIAL PRIMARY KEY, mode VARCHAR NOT NULL, map VARCHAR NOT NULL, json VARCHAR NOT NULL)")
    sqlCommand(connection, "CREATE TABLE IF NOT EXISTS telemetries (id SERIAL PRIMARY KEY, json VARCHAR NOT NULL)")

def saveUser(connection, username, userJson):
    try:
        psql_insert_query = """ INSERT INTO users (id, json) VALUES (%s, %s)"""
        record_to_insert = (username, userJson)
        getCursor(connection).execute("INSERT INTO users ('kake','kakendatat')")
    except (Exception, psycopg2.Error) as error:
        print("Failed to save user: ", error)


conn = getDBConnection("localhost", "5432", "pubgstatz", "pubgstatz", "pubgstatz")

data = query(conn, sql_command)

print(data)

initDB(conn)
saveUser(conn, "kake", "kakendatat")

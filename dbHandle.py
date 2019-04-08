import psycopg2
import pandas as pd

conn_string = "host=localhost port=5432 dbname=pubgstatz user=pubgstatz password=pubgstatz"

def getDBConnection(host, port, dbname, user, password):
    return psycopg2.connect("host="+host+" port="+port+" dbname="+dbname+ " user="+user+" password="+password)

def getCursor(connection):
    return connection.cursor()

def query(connection, queryString):
    return pd.read_sql(queryString, connection)

def sqlCommand(connection, command):
    try:
        getCursor(connection).execute(command)
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: ", error)

def initDB(connection):
    sqlCommand(connection, "CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, json VARCHAR NOT NULL)")
    sqlCommand(connection, "CREATE TABLE IF NOT EXISTS matches (id SERIAL PRIMARY KEY, mode VARCHAR NOT NULL, map VARCHAR NOT NULL, json VARCHAR NOT NULL)")
    sqlCommand(connection, "CREATE TABLE IF NOT EXISTS telemetries (id SERIAL PRIMARY KEY, json VARCHAR NOT NULL)")

def saveUserJson(connection, userId, userJson):
    try:
        if not loadUserJson(connection, userId):
            getCursor(connection).execute("INSERT INTO users VALUES("+str(userId)+",'"+userJson+"')")
            connection.commit()
        else:
            print("Error: user already exists")
    except (Exception, psycopg2.Error) as error:
        print("Failed to save user: ", error)

def loadUserJson(connection, userId):
    cursor = getCursor(connection)
    cursor.execute("SELECT * FROM users WHERE id="+str(userId))
    record = cursor.fetchall()
    if len(record) is 1:
        return True, record[0][1]
    else:
        return False

# example use case
conn = getDBConnection("localhost", "5432", "pubgstatz", "pubgstatz", "pubgstatz")
initDB(conn)
saveUserJson(conn, 236, "kakendatat")
data = query(conn, "SELECT * FROM users")
print("select * from users:")
print(data)
print("load user 234:")
print(loadUserJson(conn, 234))
print("load user 235:")
print(loadUserJson(conn,235))

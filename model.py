import json
import mysql
from MySQLdb import connect, cursors
from mysql.connector import errorcode


class Model(object):
    def __init__(self, table):
        self.table = table

        with open('settings.json', 'r') as file:
            data = json.load(file)['db']

        try:
            self.connection = connect(
                host=data['host'],
                user=data['user'],
                password=data['password'],
                database=data['database'],
                cursorclass=cursors.DictCursor)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            self.cursor = self.connection.cursor()

    async def getTimebotUser(self, uid: int) -> list:
        self.cursor.execute("SELECT * FROM timebot WHERE uid = %s", (str(uid),))
        user = self.cursor.fetchall()
        return user

    async def getUsersTimezone(self, uid: list) -> list:
        self.cursor.execute("SELECT uid, timezone FROM timebot WHERE uid IN %s", (uid,))
        users = self.cursor.fetchall()
        return users

    async def updateUserTimezone(self, uid: int, timezone: str):
        self.cursor.execute("UPDATE timebot SET timezone = %s WHERE uid = %s", (timezone, str(uid),))
        self.connection.commit()

    async def insertUserTimezone(self, uid: int, timezone: str):
        self.cursor.execute("INSERT INTO timebot (timezone, uid) VALUES (%s, %s)", (timezone, str(uid),))
        self.connection.commit()

# !/usr/bin/python3
__author__ = "u/wontfixit"
__copyright__ = "Copyright 2020"
__license__ = "GPL"
__version__ = "1.0.0"

import sqlite3
from datetime import datetime

created_at = str(datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))



class DBhelper:
    def __init__(self):

        self.database = sqlite3.connect('./ignorebase.db')
        self.c = self.database.cursor()

        return None

    def CreateTables(database, c):
        c.execute('''CREATE TABLE "Datatable" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"id_user"	TEXT,
	"name_user"	TEXT,
	"id_artist"	TEXT,
	"name_artist"	TEXT,
	"status"	INTEGER,
	"created_at"	TEXT
);''')
        database.commit()
        c.close()


    def addNewIgnore(self, id_user,name_user,id_artist,name_artist):
        status = '1'  # =locked

        try:
            self.c.execute('''INSERT OR IGNORE INTO Datatable(id_user,name_user,id_artist,name_artist,status,created_at)
						  VALUES(?,?,?,?,?,?)''', (id_user, name_user, id_artist, name_artist, status, created_at))
            self.database.commit()
            sqlquery = self.database.set_trace_callback(None)
            if sqlquery == True:

                return True
            else:

                return False
        except Exception as err:
            print(str(err))
            return False
        finally:
            None


    def updateStatus(self, id_user,id_artist, status):

        self.c.execute("UPDATE Datatable SET status = ? WHERE id_user = ? and id_artist = ?", (status, id_user, id_artist))
        self.database.commit()


    def getArtistByUser(self, id_user, id_artist):
        self.c.execute("Select count(*) from Datatable where id_user = ? and id_artist = ? and status = 1", (id_user, id_artist,))
        # self.c.execute("Select solution from Games where rID = ?",(rid,))
        self.database.commit()
        result = self.c.fetchall()

        if result[0][0] == 1:
            return True
        else:
            return False

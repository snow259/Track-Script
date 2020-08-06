import sqlite3
import os

filePath = os.path.realpath(__file__)
fileDirectory = os.path.dirname(filePath)
dataDirectory = fileDirectory + '\\Data'
backupDirectory = fileDirectory + '\\Backup'
databasePath = dataDirectory + '\\mainDatabase.db'

#Checks if database exists, creates elsewise
def checkForDataFolder():
	dirList = os.listdir(fileDirectory)
	if dirList.count('Data') == 0:
		os.mkdir(dataDirectory)

def checkForDatabase():
	dirList = os.listdir(dataDirectory)
	if dirList.count('mainDatabase.db') == 0:
		database = sqlite3.connect(databasePath)
		cursor = database.cursor()
		cursor.execute('CREATE TABLE Games (id INTEGER PRIMARY KEY, name TEXT NOT NULL, startTime TIMESTAMP, endTime TIMESTAMP, duration TIMESTAMP)')
		database.close()

#Checks for an open session
# def checkOpenSessions():

#Writes session to database
# def writeSession():

#Edits session already written, scope of editability yet to be determined
# def editSession():

#Deletes open sessions
# def deleteSession():

#Creates a backup of the database
# def backupDatabase():

checkForDataFolder()
checkForDatabase()

import sqlite3
import os
import datetime as dt

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
		cursor.execute('CREATE TABLE Games (id INTEGER PRIMARY KEY, name TEXT NOT NULL, startTime TIMESTAMP, endTime TIMESTAMP, duration TEXT)')
		database.close()

#Todo: add code for multiple open session repair, with option to select session by id, then delete or close it with entered time
#Checks for an open session
def checkOpenSessions():
	database = sqlite3.connect(databasePath)
	database.row_factory = sqlite3.Row
	cursor = database.cursor()
	cursor.execute('SELECT id, name, startTime FROM Games WHERE endTime IS ?', (None, ))
	rows = cursor.fetchall()
	# for row in rows:
	# 	print(str(row['id']) + ' ' + str(row['name']) + ' ' + str(row['startTime']))
	database.close()

	return rows

def checkDurations():
	database = sqlite3.connect(databasePath)
	database.row_factory = sqlite3.Row
	cursor = database.cursor()
	checkDurationString = 'SELECT id, startTime, endTime FROM Games WHERE startTime IS NOT NULL AND endTime IS NOT NULL AND duration IS NULL'
	cursor.execute(checkDurationString)
	rows = cursor.fetchall()
	database.close()

	return rows

def returnDatabaseContents():
	database = sqlite3.connect(databasePath)
	database.row_factory = sqlite3.Row
	cursor = database.cursor()
	cursor.execute('SELECT * FROM Games')
	rows = cursor.fetchall()
	database.close()

	return rows

#Writes session to database
def writeSession(rowId, name, startTime, endTime, duration):
	insertString = 'INSERT INTO Games VALUES(?, ?, ?, ?, ?)'
	database = sqlite3.connect(databasePath)
	cursor = database.cursor()
	cursor.execute(insertString, (rowId, name, startTime, endTime, duration))
	database.commit()
	database.close()

#Closes session in database
def closeSession(endTime):
	closeString = 'UPDATE Games SET endTime = ? WHERE endTime IS NULL'
	database = sqlite3.connect(databasePath)
	cursor = database.cursor()
	cursor.execute(closeString, (endTime, ))
	database.commit()
	database.close()

#Deletes specified sessions
def deleteSession(rowId):
	deleteString = 'DELETE FROM Games WHERE id IS ?'
	database = sqlite3.connect(databasePath)
	cursor = database.cursor()
	cursor.execute(deleteString, (rowId, ))
	database.commit()
	database.close()

def writeDuration(rowId, duration):
	print(rowId)
	print(duration)
	writeDurationString = 'UPDATE Games SET duration = ? WHERE id IS ?'
	database = sqlite3.connect(databasePath)
	cursor = database.cursor()
	cursor.execute(writeDurationString, (duration, rowId))
	database.commit()
	database.close()

#Creates a backup of the database
# def backupDatabase():

checkForDataFolder()
checkForDatabase()
# writeSession(None, 'Test3', dt.datetime.now(), None, None)
checkOpenSessions()

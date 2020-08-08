import sqlite3
import os
import datetime as dt

#All paths used
#filePath is path to this file, its directory is fileDirectory
filePath = os.path.realpath(__file__)
fileDirectory = os.path.dirname(filePath)
dataDirectory = fileDirectory + '\\Data'
backupDirectory = fileDirectory + '\\Backup'
databasePath = dataDirectory + '\\mainDatabase.db'

#Checks if folder for databases exists, creates elsewise
def checkForDataFolder():
	dirList = os.listdir(fileDirectory)
	if dirList.count('Data') == 0:
		os.mkdir(dataDirectory)

#Checks if database exists, creases elsewise
def checkForDatabase():
	dirList = os.listdir(dataDirectory)
	if dirList.count('mainDatabase.db') == 0:
		database = sqlite3.connect(databasePath)
		cursor = database.cursor()
		cursor.execute('CREATE TABLE Games (id INTEGER PRIMARY KEY, name TEXT NOT NULL, startTime TIMESTAMP, endTime TIMESTAMP, duration TEXT)')
		database.close()

#Checks for an open session
def checkOpenSessions():
	database = sqlite3.connect(databasePath)
	database.row_factory = sqlite3.Row
	cursor = database.cursor()
	cursor.execute('SELECT id, name, startTime FROM Games WHERE endTime IS ?', (None, ))
	rows = cursor.fetchall()
	database.close()

	return rows

#Finds any sessions with both times entered and duration not computed
def checkDurations():
	database = sqlite3.connect(databasePath)
	database.row_factory = sqlite3.Row
	cursor = database.cursor()
	checkDurationString = 'SELECT id, startTime, endTime FROM Games WHERE startTime IS NOT NULL AND endTime IS NOT NULL AND duration IS NULL'
	cursor.execute(checkDurationString)
	rows = cursor.fetchall()
	database.close()

	return rows

#Returns start and end times of specified session
def returnTimes(rowId):
	returnTimesString = 'SELECT startTime, endTime FROM Games WHERE id IS ?'
	database = sqlite3.connect(databasePath)
	database.row_factory = sqlite3.Row
	cursor = database.cursor()
	cursor.execute(returnTimesString, (rowId, ))
	times = cursor.fetchall()
	database.close()

	return times

def returnAllStartTimes():
	returnAllStartTimesString = 'SELECT startTime FROM Games'
	database = sqlite3.connect(databasePath)
	database.row_factory = sqlite3.Row
	cursor = database.cursor()
	cursor.execute(returnAllStartTimesString)
	startTimes = cursor.fetchall()
	database.close()

	return startTimes

#Returns all rows
def returnDatabaseContents():
	database = sqlite3.connect(databasePath)
	database.row_factory = sqlite3.Row
	cursor = database.cursor()
	cursor.execute('SELECT * FROM Games')
	rows = cursor.fetchall()
	database.close()

	return rows

#Returns single, specified row
def returnRow(rowId):
	returnRowString = 'SELECT * FROM Games WHERE id IS ?'
	database = sqlite3.connect(databasePath)
	database.row_factory = sqlite3.Row
	cursor = database.cursor()
	cursor.execute(returnRowString, (rowId, ))
	row = cursor.fetchall()
	database.close()

	return row

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

#Writes the duration of a session
def writeDuration(rowId, duration):
	writeDurationString = 'UPDATE Games SET duration = ? WHERE id IS ?'
	database = sqlite3.connect(databasePath)
	cursor = database.cursor()
	cursor.execute(writeDurationString, (duration, rowId))
	database.commit()
	database.close()

#Allows editing of the name, start, and end times of a session. Duration is recomputed after, in track.py
def modifySession(rowId, key, value):
	modifyEntryString = 'UPDATE Games SET ' + key + ' = ? WHERE id IS ?'
	database = sqlite3.connect(databasePath)
	cursor = database.cursor()
	cursor.execute(modifyEntryString, (value, int(rowId)))
	database.commit()
	database.close()

def deleteAllMain():
	deleteAllMainString = 'DELETE FROM Games'
	database = sqlite3.connect(databasePath)
	cursor = database.cursor()
	cursor.execute(deleteAllMainString)
	database.commit()
	database.close()

def vacuumMain():
	vacuumMainString = 'VACUUM'
	database = sqlite3.connect(databasePath)
	database.execute(vacuumMainString)
	database.commit()
	database.close()

checkForDataFolder()
checkForDatabase()
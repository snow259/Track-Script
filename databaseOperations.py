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
	checkOpenSessionsString = 'SELECT id, name, startTime FROM Games WHERE endTime IS ?'
	argument = (None, )
	rows = executeRead(databasePath, checkOpenSessionsString, argument, 'checkOpenSessions()')

	return rows

#Finds any sessions with both times entered and duration not computed
def checkDurations():
	checkDurationString = 'SELECT id, startTime, endTime FROM Games WHERE startTime IS NOT NULL AND endTime IS NOT NULL AND duration IS NULL'
	argument = None
	rows = executeRead(databasePath, checkDurationString, argument, 'checkDurations()')

	return rows

#Returns start and end times of specified session
def returnTimes(rowId):
	returnTimesString = 'SELECT startTime, endTime FROM Games WHERE id IS ?'
	argument = (rowId, )
	times = executeRead(databasePath, returnTimesString, argument, 'returnTimes()')

	return times

def returnAllStartTimes():
	returnAllStartTimesString = 'SELECT startTime FROM Games'
	argument = None
	startTimes = executeRead(databasePath, returnAllStartTimesString, argument, 'returnAllStartTimes()')

	return startTimes
	
#Returns all rows
def returnDatabaseContents():
	returnDatabaseContentsString = 'SELECT * FROM Games'
	argument = None
	rows = executeRead(databasePath, returnDatabaseContentsString, argument, 'returnDatabaseContents()')

	return rows

#Returns single, specified row
def returnRow(rowId):
	returnRowString = 'SELECT * FROM Games WHERE id IS ?'
	argument = (rowId, )
	row = executeRead(databasePath, returnRowString, argument, 'returnRow()')

	return row

#Writes session to database
def writeSession(rowId, name, startTime, endTime, duration):
	insertString = 'INSERT INTO Games VALUES(?, ?, ?, ?, ?)'
	argument = (rowId, name, startTime, endTime, duration)
	executeWrite(databasePath, insertString, argument, 'writeSession()')

#Closes session in database
def closeSession(endTime):
	closeString = 'UPDATE Games SET endTime = ? WHERE endTime IS NULL'
	argument = (endTime, )
	executeWrite(databasePath, closeString, argument, 'closeSession()')

#Deletes specified sessions
def deleteSession(rowId):
	deleteString = 'DELETE FROM Games WHERE id IS ?'
	argument = (rowId, )
	executeWrite(databasePath, deleteString, argument, 'deleteSession()')

#Writes the duration of a session
def writeDuration(rowId, duration):
	writeDurationString = 'UPDATE Games SET duration = ? WHERE id IS ?'
	argument = (duration, rowId)
	executeWrite(databasePath, writeDurationString, argument, 'writeDuration()')

#Allows editing of the name, start, and end times of a session. Duration is recomputed after, in track.py
def modifySession(rowId, key, value):
	modifySessionString = 'UPDATE Games SET ' + key + ' = ? WHERE id IS ?'
	argument = (value, int(rowId))
	executeWrite(databasePath, modifySessionString, argument, 'modifySession()')

#Deletes all sessions from database, done during backup
def deleteAllMain():
	deleteAllMainString = 'DELETE FROM Games'
	argument = None
	executeWrite(databasePath, deleteAllMainString, argument, 'deleteAllMain()')

#Vacuums database into another location to serve as backup
def vacuumMain():
	vacuumMainString = 'VACUUM'
	argument = None
	executeWrite(databasePath, vacuumMainString, argument, 'vacuumMain()')

#Called by all functions that read the database and return a variable
def executeRead(databasePath, commandString, argument, functionName):
	database = sqlite3.connect(databasePath)
	database.row_factory = sqlite3.Row
	cursor = database.cursor()

	try:
		if argument == None:
			cursor.execute(commandString)
		else:
			cursor.execute(commandString, argument)
	except Exception as e:
		print('Error in ' + functionName)
		print(e)
	else:
		rows = cursor.fetchall()
		return rows
	finally:
		database.close()

	return rows

#Called by all functions that modify the database
def executeWrite(databasePath, commandString, argument, functionName):
	database = sqlite3.connect(databasePath)
	cursor = database.cursor()
	try:
		if argument == None:
			cursor.execute(commandString)
		else:
			cursor.execute(commandString, argument)
	except Exception as e:
		print('Error in ' + str(functionName))
		print(e)
		print('Rolling back!')
		database.rollback()
	else:
		database.commit()
	finally:
		database.close()

checkForDataFolder()
checkForDatabase()
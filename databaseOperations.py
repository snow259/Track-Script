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
	try:
		cursor.execute('SELECT id, name, startTime FROM Games WHERE endTime IS ?', (None, ))
	except Exception as e:
		print('Error in checkOpenSessions()')
		print(e)
	else:
		rows = cursor.fetchall()
		return rows
	finally:
		database.close()

#Finds any sessions with both times entered and duration not computed
def checkDurations():
	checkDurationString = 'SELECT id, startTime, endTime FROM Games WHERE startTime IS NOT NULL AND endTime IS NOT NULL AND duration IS NULL'
	database = sqlite3.connect(databasePath)
	database.row_factory = sqlite3.Row
	cursor = database.cursor()
	try:
		cursor.execute(checkDurationString)
	except Exception as e:
		print('Error in checkDurations()')
		print(e)
	else:
		rows = cursor.fetchall()
		return rows
	finally:
		database.close()

#Returns start and end times of specified session
def returnTimes(rowId):
	returnTimesString = 'SELECT startTime, endTime FROM Games WHERE id IS ?'
	database = sqlite3.connect(databasePath)
	database.row_factory = sqlite3.Row
	cursor = database.cursor()
	try:
		cursor.execute(returnTimesString, (rowId, ))
	except Exception as e:
		print('Error in returnTimes()')
		print(e)
	else:
		times = cursor.fetchall()
		return times
	finally:
		database.close()

def returnAllStartTimes():
	returnAllStartTimesString = 'SELECT startTime FROM Games'
	database = sqlite3.connect(databasePath)
	database.row_factory = sqlite3.Row
	cursor = database.cursor()
	try:
		cursor.execute(returnAllStartTimesString)
	except Exception as e:
		print('Error in returnAllStartTimes()')
		print(e)
	else:
		startTimes = cursor.fetchall()
		return startTimes
	finally:
		database.close()

#Returns all rows
def returnDatabaseContents():
	database = sqlite3.connect(databasePath)
	database.row_factory = sqlite3.Row
	cursor = database.cursor()
	try:
		cursor.execute('SELECT * FROM Games')
	except Exception as e:
		print('Error in returnDatabaseContents()')
		print(e)
	else:
		rows = cursor.fetchall()
		return rows
	finally:
		database.close()

#Returns single, specified row
def returnRow(rowId):
	returnRowString = 'SELECT * FROM Games WHERE id IS ?'
	database = sqlite3.connect(databasePath)
	database.row_factory = sqlite3.Row
	cursor = database.cursor()
	try:
		cursor.execute(returnRowString, (rowId, ))
	except Exception as e:
		print('Error in returnRow()')
		print(e)
	else:
		row = cursor.fetchall()
		return row
	finally:
		database.close()

#Writes session to database
def writeSession(rowId, name, startTime, endTime, duration):
	insertString = 'INSERT INTO Games VALUES(?, ?, ?, ?, ?)'
	database = sqlite3.connect(databasePath)
	cursor = database.cursor()
	try:
		cursor.execute(insertString, (rowId, name, startTime, endTime, duration))
	except Exception as e:
		print('Error in writeSession()')
		print(e)
		print('Rolling back!')
		database.rollback()
	else:
		database.commit()
	finally:
		database.close()

#Closes session in database
def closeSession(endTime):
	closeString = 'UPDATE Games SET endTime = ? WHERE endTime IS NULL'
	database = sqlite3.connect(databasePath)
	cursor = database.cursor()
	try:
		cursor.execute(closeString, (endTime, ))
	except Exception as e:
		print('Error in closeSession()')
		print(e)
		print('Rolling back!')
		database.rollback()
	else:
		database.commit()
	finally:
		database.close()

#Deletes specified sessions
def deleteSession(rowId):
	deleteString = 'DELETE FROM Games WHERE id IS ?'
	database = sqlite3.connect(databasePath)
	cursor = database.cursor()
	try:
		cursor.execute(deleteString, (rowId, ))
	except Exception as e:
		print('Error in deleteSession()')
		print(e)
		print('Rolling back!')
		database.rollback()
	else:
		database.commit()
	finally:
		database.close()

#Writes the duration of a session
def writeDuration(rowId, duration):
	writeDurationString = 'UPDATE Games SET duration = ? WHERE id IS ?'
	database = sqlite3.connect(databasePath)
	cursor = database.cursor()
	try:
		cursor.execute(writeDurationString, (duration, rowId))
	except Exception as e:
		print('Error in writeDuration()')
		print(e)
		print('Rolling back!')
		database.rollback()
	else:
		database.commit()
	finally:
		database.close()

#Allows editing of the name, start, and end times of a session. Duration is recomputed after, in track.py
def modifySession(rowId, key, value):
	modifyEntryString = 'UPDATE Games SET ' + key + ' = ? WHERE id IS ?'
	database = sqlite3.connect(databasePath)
	cursor = database.cursor()
	try:
		cursor.execute(modifyEntryString, (value, int(rowId)))
	except Exception as e:
		print('Error in modifySession()')
		print(e)
		print('Rolling back!')
		database.rollback()
	else:
		database.commit()
	finally:
		database.close()

def deleteAllMain():
	deleteAllMainString = 'DELETE FROM Games'
	database = sqlite3.connect(databasePath)
	cursor = database.cursor()
	try:
		cursor.execute(deleteAllMainString)
	except Exception as e:
		print('Error in deleteAllMain()')
		print(e)
		print('Rolling back!')
		database.rollback()
	else:
		database.commit()
	finally:
		database.close()

def vacuumMain():
	vacuumMainString = 'VACUUM'
	database = sqlite3.connect(databasePath)
	try:
		database.execute(vacuumMainString)
	except Exception as e:
		print('Error in vacuumMain()')
		print(e)
	finally:
		database.close()

checkForDataFolder()
checkForDatabase()
import os
import sqlite3

filePath = os.path.realpath(__file__)
fileDirectory = os.path.dirname(filePath)
databasePath = fileDirectory + '\\legacyData.db'

def returnMidnightEnd():
	returnMidnightEndString = 'SELECT * FROM GAMES WHERE endTime LIKE "%23:59:00%"'
	argument = None
	midnightEnd = executeRead(databasePath, returnMidnightEndString, argument, 'returnMidnightEnd()')

	return midnightEnd

def returnMidnightStart():
	returnMidnightStartString = 'SELECT * FROM GAMES WHERE startTime LIKE "%00:00:00%"'
	argument = None
	midnightStart = executeRead(databasePath, returnMidnightStartString, argument, 'returnMidnightStart()')

	return midnightStart

#Allows editing of the name, start, and end times of a session. Duration is recomputed after, in track.py
def modifySession(session):
	rowId = session['id']
	startTime = session['startTime']
	endTime = session['endTime']
	duration = session['duration']
	modifySessionString = 'UPDATE Games SET startTime = ?, endTime = ?, duration = ? WHERE id IS ?'
	argument = (startTime, endTime, str(duration), int(rowId))
	executeWrite(databasePath, modifySessionString, argument, 'modifySession()')

#Deletes specified sessions
def deleteSession(rowId):
	deleteString = 'DELETE FROM Games WHERE id IS ?'
	argument = (rowId, )
	executeWrite(databasePath, deleteString, argument, 'deleteSession()')

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
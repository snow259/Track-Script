import sqlite3
import os

filePath = os.path.realpath(__file__)
fileDirectory = os.path.dirname(filePath)
dirList = os.listdir(fileDirectory)

databaseName = 'ultraLegacyData.db'
databasePath = fileDirectory + '\\' + databaseName

def createDataBase():
	if databaseName not in dirList:
		database = sqlite3.connect(databasePath)
		cursor = database.cursor()
		cursor.execute('CREATE TABLE Games (id INTEGER PRIMARY KEY, name TEXT NOT NULL, date TIMESTAMP, duration TIMESTAMP)')
		database.close()

def writeSession(row):
	writeSessionString = 'INSERT INTO Games VALUES(?, ?, ?, ?)'
	rowId = None
	name = row['name']
	date = row['startTime']
	duration = row['duration']
	argument = (rowId, name, date, duration)
	executeWrite(databasePath, writeSessionString, argument, 'writeSession()')

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
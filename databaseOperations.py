import sqlite3
import os

# All paths used
# filePath is path to this file, its directory is fileDirectory
filePath = os.path.realpath(__file__)
fileDirectory = os.path.dirname(filePath)
dataDirectory = fileDirectory + '\\Data'
backupDirectory = fileDirectory + '\\Backup'
databasePath = dataDirectory + '\\mainDatabase.db'
archivePath = dataDirectory + '\\archiveDatabase.db'

# Path to and presence of legacy data. Any statistics of games computed will check for legacy data
oldDatabasesDirectory = fileDirectory + '\\Old\\Databases'
legacyPath = oldDatabasesDirectory + '\\ultraLegacyDataProcessed.db'
legacyDataPresent = False
if 'Old' in os.listdir(fileDirectory):
	if 'Databases' in os.listdir(fileDirectory + '\\Old'):
		if 'ultraLegacyDataProcessed.db' in os.listdir(oldDatabasesDirectory):
			legacyDataPresent = True


# Setup functions
# Checks if folder for databases exists, creates one elsewise
def checkForDataFolder():
	dirList = os.listdir(fileDirectory)
	if dirList.count('Data') == 0:
		os.mkdir(dataDirectory)


# Checks if database exists, creates one elsewise
def checkForDatabase():
	dirList = os.listdir(dataDirectory)
	if dirList.count('mainDatabase.db') == 0:
		database = sqlite3.connect(databasePath)
		cursor = database.cursor()
		cursor.execute('CREATE TABLE Games (id INTEGER PRIMARY KEY, name TEXT NOT NULL, startTime TIMESTAMP, endTime TIMESTAMP, duration TEXT)')
		cursor.execute('CREATE TABLE Timezones (id INTEGER PRIMARY KEY, startTimeTzOffset INTEGER, startTimeTzName TEXT, endTimeTzOffset Integer, endTimeTzName TEXT)')
		database.close()


# Database read functions
# Checks for an open session
def checkOpenSessions():
	checkOpenSessionsString = 'SELECT id, name, startTime FROM Games WHERE endTime IS ?'
	argument = (None, )
	rows = executeRead(databasePath, [checkOpenSessionsString], [argument], 'checkOpenSessions()')[0]

	return rows


# Finds any sessions with both times entered and duration not computed
def checkDurations():
	checkDurationString = 'SELECT id, startTime, endTime FROM Games WHERE startTime IS NOT NULL AND endTime IS NOT NULL AND duration IS NULL'
	argument = None
	rows = executeRead(databasePath, [checkDurationString], [argument], 'checkDurations()')[0]

	return rows


# Returns start and end times of specified session
def returnTimes(rowId):
	returnTimesString = 'SELECT startTime, endTime FROM Games WHERE id IS ?'
	argument = (rowId, )
	times = executeRead(databasePath, [returnTimesString], [argument], 'returnTimes()')[0]

	return times


def returnAllStartTimes():
	returnAllStartTimesString = 'SELECT startTime FROM Games'
	argument = None
	startTimes = executeRead(databasePath, [returnAllStartTimesString], [argument], 'returnAllStartTimes()')[0]

	return startTimes


# Returns all rows
def returnDatabaseContents():
	returnDatabaseContentsString = 'SELECT * FROM Games'
	argument = None
	rows = executeRead(databasePath, [returnDatabaseContentsString], [argument], 'returnDatabaseContents()')[0]

	return rows


# Returns single, specified row
def returnRow(rowId):
	returnRowString = 'SELECT * FROM Games WHERE id IS ?'
	argument = (rowId, )
	row = executeRead(databasePath, [returnRowString], [argument], 'returnRow()')[0]

	return row


# Returns list of table names from the database
def returnTablesList():
	returnTableListString = 'SELECT name FROM sqlite_master WHERE type = "table"'
	argument = None
	rows = executeRead(databasePath, [returnTableListString], [argument], 'createTable()')[0]
	tables = []
	for row in rows:
		# Here, the contents of the sqlite3.Row object is extracted. I have no idea what the key for this is, else this would be neater to code
		for element in row:
			tables.append(element)

	return tables


# Returns all rows from archive database
def returnArchiveContents():
	returnArchiveContentsString = 'SELECT * FROM Games'
	argument = None
	rows = executeRead(archivePath, [returnArchiveContentsString], [argument], 'returnArchiveContents()')[0]

	return rows


# Return rows from main database containing specified game
def returnGameMain(name):
	returnGameMainString = 'SELECT * FROM Games WHERE name IS ?'
	argument = (name,)
	rows = executeRead(databasePath, [returnGameMainString], [argument], 'returnGameMain()')[0]

	return rows


# Return rows from archive database containing specified game
def returnGameArchive(name):
	returnGameArchiveString = 'SELECT * FROM Games WHERE name IS ?'
	argument = (name,)
	rows = executeRead(archivePath, [returnGameArchiveString], [argument], 'returnGameArchive()')[0]

	return rows


def returnGameLife():
	returnGameLifeString = 'SELECT * FROM GameLife'
	argument = None
	rows = executeRead(databasePath, [returnGameLifeString], [argument], 'returnGameLife()')[0]

	return rows


def returnGameLifeSorted():
	returnGameLifeSortedString = 'SELECT id, name, lastPlayed FROM GameLife ORDER BY lastPlayed DESC'
	argument = None
	rows = executeRead(databasePath, [returnGameLifeSortedString], [argument], 'returnGameLifeSorted()')[0]

	return rows


def returnTotalTimePlayed():
	queries = list()
	arguments = list()

	attachMainDataString = 'ATTACH ? as m;'
	attachMainDataArgument = (databasePath,)

	queries.append(attachMainDataString)
	arguments.append(attachMainDataArgument)

	if legacyDataPresent:
		attachLegacyDataString = 'ATTACH ? as e;'
		attachLegacyDataArgument = (legacyPath,)

		queries.append(attachLegacyDataString)
		arguments.append(attachLegacyDataArgument)

	returnTotalTimePlayedString = """
	SELECT	t.name,
			t.hours||':'||(SUBSTR('00'||t.minutes, -2, 2)) AS timePlayed,
			t.count,
			(SUBSTR('00'||((t.totalMinutes/t.count)/60), -2, 2))||':'||(SUBSTR('00'||((t.totalMinutes/t.count)%60), -2, 2)) as averageTimePlayed

	FROM
	(
		SELECT	name,
				(SUM((strftime('%s', endTime) - strftime('%s', startTime)))/3600) AS hours,
				(SUM((strftime('%s', endTime) - strftime('%s', startTime)))/60%60) AS minutes,
				(SUM((strftime('%s', endTime) - strftime('%s', startTime)))/60) AS totalMinutes,
				COUNT(name) as count

		FROM
		(
			SELECT name, startTime, endTime
			FROM Games

			UNION ALL

			SELECT name, startTime, endTime
			FROM m.Games

	"""

	# Selects data from legacy database
	if legacyDataPresent:
		returnTotalTimePlayedString += """
		UNION ALL

		SELECT name, startTime, endTime
		FROM e.Games
		"""

	returnTotalTimePlayedString += """
		)
		GROUP BY name
	) AS t

	ORDER BY hours DESC, minutes DESC, count DESC
	"""
	returnTotalTimePlayedArgument = None

	queries.append(returnTotalTimePlayedString)
	arguments.append(returnTotalTimePlayedArgument)

	rowsList = executeRead(archivePath, queries, arguments, 'returnTotalTimePlayed()')

	# The only query that selects rows is the last one that returns the required data
	# This is required as there may be two or three queries that go to the database
	for item in rowsList:
		if len(item) > 0:
			rows = item
			break

	return rows


# Database write functions
# Writes session to database
def writeSession(gameInfo, tzInfo):
	insertGameString = 'INSERT INTO Games VALUES(?, ?, ?, ?, ?)'
	insertGameArgument = (gameInfo['rowId'], gameInfo['name'], gameInfo['startTime'], gameInfo['endTime'], gameInfo['duration'])

	insertTzString = 'INSERT INTO Timezones VALUES(?, ?, ?, ?, ?)'
	insertTzArgument = (tzInfo['rowId'], tzInfo['startTimeTzOffset'], tzInfo['startTimeTzName'], tzInfo['endTimeTzOffset'], tzInfo['endTimeTzName'])

	executeWrite(databasePath, [insertGameString, insertTzString], [insertGameArgument, insertTzArgument], 'writeSession()')


# Closes session in database
def closeSession(endTime, tzInfo):
	closeGameString = 'UPDATE Games SET endTime = ? WHERE endTime IS NULL'
	closeGameArgument = (endTime,)

	closeTzString = 'UPDATE Timezones SET endTimeTzOffset = ?, endTimeTzName = ? WHERE endTimeTzOffset IS NULL'
	closeTzArgument = (tzInfo['endTimeTzOffset'], tzInfo['endTimeTzName'])

	executeWrite(databasePath, [closeGameString, closeTzString], [closeGameArgument, closeTzArgument], 'closeSession()')


# Deletes specified sessions
def deleteSession(rowId):
	deleteGamesString = 'DELETE FROM Games WHERE id IS ?'
	argument = (rowId, )
	deleteTzString = 'DELETE FROM Timezones WHERE id IS ?'
	executeWrite(databasePath, [deleteGamesString, deleteTzString], [argument, argument], 'deleteSession()')


# Writes the duration of a session
def writeDuration(rowId, duration):
	writeDurationString = 'UPDATE Games SET duration = ? WHERE id IS ?'
	argument = (duration, rowId)
	executeWrite(databasePath, [writeDurationString], [argument], 'writeDuration()')


# Allows editing of the name, start, and end times of a session. Duration is recomputed after, in track.py
def modifySession(rowId, key, value):
	modifySessionString = 'UPDATE Games SET ' + key + ' = ? WHERE id IS ?'
	argument = (value, int(rowId))
	executeWrite(databasePath, [modifySessionString], [argument], 'modifySession()')


# Deletes all sessions from database, done during backup
def deleteAllMain():
	deleteAllMainGamesString = 'DELETE FROM Games'
	deleteAllMainGamesArgument = None
	deleteAllMainTzString = 'DELETE FROM Timezones'
	deleteAllMainTzArgument = None
	executeWrite(databasePath, [deleteAllMainGamesString, deleteAllMainTzString], [deleteAllMainGamesArgument, deleteAllMainTzArgument], 'deleteAllMain()')


# Vacuums database into another location to serve as backup
def vacuumMain():
	vacuumMainString = 'VACUUM'
	argument = None
	executeWrite(databasePath, [vacuumMainString], [argument], 'vacuumMain()')


# Creates the table GameLife to store all game lives
def createGameLifeTable():
	createLastPlayedTableString = 'CREATE TABLE GameLife (id INTEGER PRIMARY KEY, name TEXT NOT NULL, firstPlayed TIMESTAMP, lastPlayed TIMESTAMP)'
	argument = None
	executeWrite(databasePath, [createLastPlayedTableString], [argument], 'createGameLifeTable()')


# Adds new game to the table
def addGameToGameLifeTable(name, firstPlayed, lastPlayed):
	addGameLastPlayedTableString = 'INSERT INTO GameLife VALUES(?, ?, ?, ?)'
	argument = (None, name, firstPlayed, lastPlayed)
	executeWrite(databasePath, [addGameLastPlayedTableString], [argument], 'addGameToGameLifeTable()')


# Edits existing game life
def updateGameLife(name, key, value):
	updateLastPlayedString = 'UPDATE GameLife SET ' + key + ' = ? WHERE name IS ?'
	argument = (value, name)
	executeWrite(databasePath, [updateLastPlayedString], [argument], 'updateGameLife()')


def deleteGameLife(name):
	deleteGameLifeString = 'DELETE FROM GameLife WHERE name IS ?'
	argument = (name, )
	executeWrite(databasePath, [deleteGameLifeString], [argument], 'deleteGameLife()')


# Called by all functions that read the database and return a variable
# def executeRead(databasePath, commandString, argument, functionName):
# 	database = sqlite3.connect(databasePath)
# 	database.row_factory = sqlite3.Row
# 	cursor = database.cursor()

# 	try:
# 		if argument is None:
# 			cursor.execute(commandString)
# 		else:
# 			cursor.execute(commandString, argument)
# 	except Exception as e:
# 		print('Error in ' + functionName)
# 		print(e)
# 	else:
# 		rows = cursor.fetchall()
# 		return rows
# 	finally:
# 		database.close()


def executeRead(databasePath, commandStrings, arguments, functionName):
	database = sqlite3.connect(databasePath)
	database.row_factory = sqlite3.Row
	cursor = database.cursor()
	rowsList = list()
	try:
		for commandString, argument in zip(commandStrings, arguments):
			if argument is None:
				cursor.execute(commandString)
			else:
				cursor.execute(commandString, argument)

			rows = cursor.fetchall()
			rowsList.append(rows)
	except Exception as e:
		print('Error in ' + functionName)
		print(e)
	else:
		return rowsList
	finally:
		database.close()


# Called by all functions that modify the database
def executeWrite(databasePath, commandStrings, arguments, functionName):
	database = sqlite3.connect(databasePath)
	cursor = database.cursor()
	try:
		for commandString, argument in zip(commandStrings, arguments):
			if argument is None:
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

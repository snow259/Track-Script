import datetime as dt
import os
import databaseOperations as dataops
import storageOperations as storeops
import timeFunctions as tf
import dataInputAndValidity as di
import output as op
import commands as cmd

# All paths used
# filePath is path to this file, its directory is fileDirectory
filePath = os.path.realpath(__file__)
fileDirectory = os.path.dirname(filePath)
dataDirectory = fileDirectory + '\\Data'
backupDirectory = fileDirectory + '\\Backup'
databasePath = dataDirectory + '\\mainDatabase.db'


# Checks database for open sessions
def checkSession():
	rows = dataops.checkOpenSessions()

	return rows


def multipleSessionRepairChoice(rows):
	print('Multiple open sessions found:')
	op.printOutput(rows)

	repairOption = ''
	while repairOption != 'close' and repairOption != 'delete':
		repairOption = input('Repair options: close, delete\n')

	return repairOption


def checkDuration():
	rows = dataops.checkDurations()
	if len(rows) > 0:
		for row in rows:
			rowId = row['id']
			calculateDuration(rowId)


def calculateDuration(rowId):
	times = dataops.returnTimes(rowId)
	startTime = times[0]['startTime']
	endTime = times[0]['endTime']
	startTime = tf.stringToDatetime(startTime)
	endTime = tf.stringToDatetime(endTime)
	duration = str(endTime - startTime)
	dataops.writeDuration(rowId, duration)


# Takes input from user, reads current time
def userInput():
	inputString = di.nameInput('\nEnter game: ')
	gameTime = dt.datetime.now()

	timezone = gameTime.astimezone()
	gameTime = tf.processDateTime(gameTime)

	return inputString, gameTime, timezone


def writeStart(inputString, gameTime, timezone):
	gameInfo = {
		'rowId': None,
		'name': inputString,
		'startTime': gameTime,
		'endTime': None,
		'duration': None,
	}

	tzInfo = {
		'rowId': None,
		'startTimeTzOffset': timezone.utcoffset().seconds,
		'startTimeTzName': timezone.tzname(),
		'endTimeTzOffset': None,
		'endTimeTzName': None,
	}

	if timezone.utcoffset().days == -1:
		tzInfo['startTimeTzOffset'] = - tzInfo['startTimeTzOffset']
	# dataops.writeSession(rowId=None, name=inputString, startTime=gameTime, endTime=None, duration=None)
	dataops.writeSession(gameInfo, tzInfo)


def inputEnd(rowId):
	choiceList = ['close', 'restart', 'input', 'delete']

	choiceString = None
	choice = di.keyInput(choiceList, choiceString)
	endTime = dt.datetime.now()

	timezone = endTime.astimezone()
	endTime = tf.processDateTime(endTime)

	if choice == 'close':
		tzInfo = {
			'endTimeTzOffset': timezone.utcoffset().seconds,
			'endTimeTzName': timezone.tzname(),
		}

		if timezone.utcoffset().days == -1:
			tzInfo['endTimeTzOffset'] = - tzInfo['endTimeTzOffset']
		dataops.closeSession(endTime, tzInfo)

	elif choice == 'restart':
		startTime = tf.processDateTime(dt.datetime.now())
		key = 'startTime'
		dataops.modifySession(rowId, key, startTime)

	elif choice == 'input':
		endTime = userInputEndTime()
		if endTime == '/cancel':
			choice = '/cancel'

	elif choice == 'delete':
		deleteSession(rowId)

	return choice


def userInputEndTime(rowId=None):
	inputCorrect = False
	while inputCorrect is False:
		userEndTime = di.timeInput(None, 'Enter end time in format: YYYY-MM-DD HH:MM:SS\n', 'endTime')
		timezone = dt.datetime.now().astimezone()
		if userEndTime != '/cancel':
			isThisRightString = 'Entered time is: ' + userEndTime + '. Is this satisfactory?'
			isThisRight = di.ynChoiceInput(isThisRightString)
			if isThisRight:
				inputCorrect = True
		else:
			return '/cancel'

	# rowId defaults to None, and session is closed via closeSession as normal
	# If rowId is provided, modifySession is used instead to edit endTime
	if userEndTime != '/cancel':
		endTime = tf.stringToDatetime(userEndTime)
		if rowId is None:
			tzInfo = {
				'endTimeTzOffset': timezone.utcoffset().seconds,
				'endTimeTzName': timezone.tzname(),
			}

			if timezone.utcoffset().days == -1:
				tzInfo['endTimeTzOffset'] = - tzInfo['endTimeTzOffset']
			dataops.closeSession(endTime, tzInfo)
			return endTime
		elif rowId is not None:
			key = 'endTime'
			dataops.modifySession(rowId, key, endTime)


# Prints all sessions into console
# If no rows present, prints that out, followed by recent games
def listSessions():
	rows = dataops.returnDatabaseContents()
	if len(rows) == 0:
		print('No sessions found in database')
		arguments = None
		cmd.recentCommand(arguments)
	if len(rows) > 0:
		op.printOutput(rows)
		return rows


# Input here must be a list even if the number of rowId is 1
# If input is a string, it will iterate through the string and split up a single number into multiple digits
def listSpecificSessions(rowIds):
	rowsRaw = []
	for rowId in rowIds:
		rowsRaw.append(dataops.returnRow(rowId))

	# Each query to the database returns a list of sqlite3.Row objects. Here, a query is one rowId
	# Thus, one list for each sqlite3.Row object is returned
	# Furthermore, unlike in listSessions, each list that is returned is appended to another list
	# Whereas the list rows in listSessions is the list returned by the query
	# The following changes the structure of rowsRaw to match that of rows in listSessions
	rows = []
	for element in rowsRaw:
		# These if checks are to prevent a crash when deleting an entry
		if len(rowsRaw[0]) == 0:
			rows.append(element)
		else:
			rows.append(element[0])

	if len(rows[0]) == 0:
		listSessions()
	else:
		op.printOutput(rows)
		return rows


# Checks for cancel in every input prior to proceeding, can select session via id and edit name and times
def editSession():
	rowId = di.rowIdInput('Enter id of session to be modified: ', multipleRowIds=False)[0]
	# If not cancel, proceed with rest of function
	if rowId != '/cancel':
		listSpecificSessions([rowId])
		keyList = ['name', 'startTime', 'endTime']
		key = di.keyInput(keyList, inputString=None)

		# If key not cancel, proceed with accepting new value
		if key != '/cancel':
			if key == 'name':
				value = di.nameInput('Enter new value: ')

			if key == 'startTime':
				value = di.timeInput(rowId, 'Enter new startTime: ', 'startTime')

			if key == 'endTime':
				value = di.timeInput(rowId, 'Enter new endTime: ', 'endTime')

			if value != '/cancel':
				dataops.modifySession(rowId, key, value)

				if key == 'startTime' or key == 'endTime':
					calculateDuration(rowId)

				return rowId, key, value


# If rowId is none, user input is taken. If it is not none, specified row is deleted
def deleteSession(rowId=None):
	if rowId is None:
		rowIds = di.rowIdInput('Ender ids to delete: ', multipleRowIds=True)

		if '/cancel' not in rowIds:
			for i in range(0, len(rowIds)):
				rowIds[i] = int(rowIds[i])

			print('The following sessions will be deleted: ')
			listSpecificSessions(rowIds)
			proceed = di.ynChoiceInput('Proceed?')
			if proceed:
				for rowId in rowIds:
					dataops.deleteSession(rowId)
				return rowIds
	else:
		dataops.deleteSession(rowId)
		return [rowId]		# The other if branch returns a list, thus this shall too

	# checkSession() #I am not sure what this is doing here


# Checks if backupInterval days has passed from any startTime within the database.
def backup(backupInterval):
	today = dt.date.today()
	mustBackup = False

	rows = dataops.returnAllStartTimes()
	if len(rows) >= 1:
		for row in rows:
			startTime = row['startTime']
			startTime = tf.stringToDatetime(startTime)
			difference = tf.dateDifference(today, startTime)

			if difference.days >= backupInterval:
				mustBackup = True
				break

	return mustBackup


# Run functions to back up archiveDatabase, archive contents of mainDatabase, then backup it too
def runBackupOperations():
	backupMainPath = generateBackupPath('Main')
	backupArchivePath = generateBackupPath('Archive')
	storeops.backupArchive(backupArchivePath)
	storeops.archive()
	storeops.backupMain(backupMainPath)
	dataops.deleteAllMain()
	dataops.vacuumMain()


# Generates a path and file name for runBackupOperations
def generateBackupPath(backupName):
	now = dt.datetime.now()
	pathSuffix = tf.datetimeToString(now)
	backupPath = '"' + backupDirectory + '\\' + backupName + '\\' + pathSuffix + '.db"'

	return backupPath

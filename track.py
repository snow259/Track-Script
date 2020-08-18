import datetime as dt
import os
import calendar
import databaseOperations as dataops
import storageOperations as storeops
import timeFunctions as tf
import output as op

#All paths used
#filePath is path to this file, its directory is fileDirectory
filePath = os.path.realpath(__file__)
fileDirectory = os.path.dirname(filePath)
dataDirectory = fileDirectory + '\\Data'
backupDirectory = fileDirectory + '\\Backup'
databasePath = dataDirectory + '\\mainDatabase.db'

#Checks database for open sessions
def checkSession():
	rows = dataops.checkOpenSessions()

	return rows

def printOpenSession(row, repair = False):
	rowId = row['id']
	game = row['name']
	startTime = row['startTime']

	if repair == False:
		outString = 'Open session:\n' + str(game) + ' ' + str(startTime)
	elif repair == True:
		outString = str(rowId) + ' ' + str(game) + ' ' + str(startTime)

	print(outString)


def multipleSessionRepairChoice(rows):
	print('Multiple open sessions found:')
	for row in rows:
		printOpenSession(row, repair = True)

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

#Takes input from user, reads current time
def userInput():
	inputString = input('Enter game: ')
	dateAndTimeRaw = dt.datetime.now()
	gameTime = tf.roundTime(dateAndTimeRaw)
	gameTime = tf.removeSeconds(gameTime)

	return inputString, gameTime

def writeStart(inputString, gameTime):
	dataops.writeSession(None, inputString, gameTime, None, None)

def inputEnd(rowId):
	choice = ''
	while choice != 'close' and  choice != 'delete' and choice != 'input':
		choice = input('Options: close, delete, input\n')
	endTime = tf.roundTime(dt.datetime.now())
	endTime = tf.removeSeconds(endTime)

	if choice == 'close':
		dataops.closeSession(endTime)
	elif choice == 'delete':
		deleteSession(rowId)
	elif choice == 'input':
		userInputEndTime()

def userInputEndTime(rowId = None):
	inputCorrect = False
	while inputCorrect == False:
		userEndTime = input('Enter end time in format: YYYY-MM-DD HH:MM:SS\n')
		userEndTime = userEndTime.strip()
		isThisRightString = 'Entered time is: ' + userEndTime + '. Is this satisfactory? (y/n)'
		isThisRight = input(isThisRightString)
		if isThisRight == 'y':
			inputCorrect = True

	#Processes input time for insertion
	userEndTime = tf.stringToDatetime(userEndTime)
	userEndTime = tf.roundTime(userEndTime)
	endTime = tf.removeSeconds(userEndTime)

	#rowId defaults to None, and session is closed via closeSession as normal. If rowId is provided, modifySession is used instead to edit endTime
	if rowId == None:
		dataops.closeSession(endTime)
	elif rowId != None:
		key = 'endTime'
		dataops.modifySession(rowId, key, endTime)

#Prints sessions into console, all if no input is given, listed rowIds elsewise
def listSessions():
	rows = dataops.returnDatabaseContents()
	if len(rows) == 0:
		print('No sessions found in database')
	if len(rows) > 0:
		op.printOutput(rows)

#Input here must be a list even if the number of rowId is 1
#If input is a string, it will iterate through the string and split up a single number into multiple digits
def listSpecificSessions(rowIds):
	rowsRaw = []
	for rowId in rowIds:
		rowsRaw.append(dataops.returnRow(rowId))

	#Each query to the database returns a list of sqlite3.Row objects. Here, a query is one rowId
	#Thus, one list for each sqlite3.Row object is returned
	#Furthermore, unlike in listSessions, each list that is returned is appended to another list
	#Whereas the list rows in listSessions is the list returned by the query
	#The following changes the structure of rowsRaw to match that of rows in listSessions
	rows = []
	for element in rowsRaw:
		rows.append(element[0])

	if len(rows[0]) == 0:
		listSessions()
	else:
		op.printOutput(rows)

#Returns a string of a row for printing in listSessions
def rowString(row):
	rowId = 'id: ' + str(row['id'])
	name = 'name: ' + str(row['name'])
	startTime = 'start: ' + str(row['startTime'])
	endTime = 'end: ' + str(row['endTime'])
	duration = 'duration: ' + str(row['duration'])
	rowString = ''
	listOfElements = [rowId, name, startTime, endTime, duration]
	for element in listOfElements:
		rowString = rowString + element + '	' #A tab is added here, not space

	return rowString

#Checks for cancel in every input prior to proceeding, can select session via id and edit name and times
def editSession():
	rowId = ''
	validRowIdType = False
	while validRowIdType == False:
		rowId = input('Enter id of session to be modified: ')

		if rowId == 'cancel':
			break

		try:
			_ = int(rowId)
		except Exception:
			pass
		else:
			validRowIdType = True

	#If not cancel, proceed with rest of function
	if rowId != 'cancel':
		listSpecificSessions([rowId])
		validKey = False
		keys = ['name', 'startTime', 'endTime', 'cancel']
		while validKey == False:
			key = input('Enter key (name, startTime, endTime): ')
			if keys.count(key) == 1:
				validKey = True

		#If key not cancel, proceed with accepting new value
		if key != 'cancel':
			value = input('Enter new value: ')

			if key == 'startTime' or key == 'endTime':
				value = tf.roundTime(value)
				value = tf.removeSeconds(value)
			
			if key != 'cancel':
				dataops.modifySession(rowId, key, value)

			if key == 'startTime' or key == 'endTime':
				calculateDuration(rowId)

			print('Edited session now is:')
			listSpecificSessions([rowId])

#If rowId is none, user input is taken. If it is not none, specified row is deleted
def deleteSession(rowId = None):
	if rowId == None:
		rowIdRaw = input('Enter ids to delete: ')
		if rowIdRaw != 'cancel':
			rowIds = rowIdRaw.split()
			print('The following sessions will be deleted: ')
			listSpecificSessions(rowIds)
			proceed = input('Proceed? (y/n)')
			if proceed == 'y':
				for rowId in rowIds:
					dataops.deleteSession(int(rowId))
	else:
		dataops.deleteSession(rowId)

	checkSession()

#Checks if backupInterval days has passed from any startTime within the database.
def backup(backupInterval):
	today = dt.date.today()

	rows = dataops.returnAllStartTimes()
	if len(rows) >= 1:
		for row in rows:
			startTime = row['startTime']
			startTime = tf.stringToDatetime(startTime)
			difference = tf.dateDifference(today, startTime)

			if difference.days >= backupInterval:
				runBackupOperations()
				break

#Generates a path and file name for runBackupOperations
def generateBackupPath(backupName):
	now = dt.datetime.now()
	pathSuffix = tf.datetimeToString(now)
	backupPath = '"' + backupDirectory + '\\' + backupName + '\\' + pathSuffix + '.db"'

	return backupPath

#Runs functions to back up archiveDatabase, archive contents of mainDatabase, then backup it too
def runBackupOperations():
	backupMainPath = generateBackupPath('Main')
	backupArchivePath = generateBackupPath('Archive')
	storeops.backupArchive(backupArchivePath)
	storeops.archive()
	storeops.backupMain(backupMainPath)
	dataops.deleteAllMain()
	dataops.vacuumMain()
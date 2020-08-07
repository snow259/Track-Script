import datetime as dt
import calendar
import databaseOperations as dataops
import timeFunctions as tf

#Checks database for open session of game, attempts repair if more than one open session is discovered
def checkSession():
	rows = dataops.checkOpenSessions()
	if len(rows) == 0:
		checkDuration()
		inputStart()

	if len(rows) == 1:
		row = rows[0]
		rowId = row['id']
		game = row['name']
		startTime = row['startTime']
		print('Open session:\n' + str(game) + ' ' + str(startTime))

		inputEnd(rowId)

	if len(rows) > 1:
		print('Multiple open sessions found:')
		for row in rows:
			rowId = row['id']
			game = row['name']
			startTime = row['startTime']
			outString = str(rowId) + ' ' + str(game) + ' ' + str(startTime)
			print(outString)
		# print('Repair options: close, delete')
		repairOption = ''
		while repairOption != 'close' and repairOption != 'delete':
			repairOption = input('Repair options: close, delete\n')

		# if repairOption == 'close':

		if repairOption == 'delete':
			deleteSession()

def checkDuration():
	rows = dataops.checkDurations()
	if len(rows) > 0:
		for row in rows:
			rowId = row['id']
			# startTime = row['startTime']
			# endTime = row['endTime']
			calculateDuration(rowId)


#Takes input from user, reads current time
def inputStart():
	inputString = input('Enter game: ')
	dateAndTimeRaw = dt.datetime.now()
	gameTime = tf.roundTime(dateAndTimeRaw)
	gameTime = tf.removeSeconds(gameTime)

	if inputString == 'edit':
		listSessions()
		editSession()
	elif inputString == 'delete':
		listSessions()
		deleteSession()
	elif inputString == 'list':
		listSessions()
	elif inputString == 'exit':
		pass
	else:
		dataops.writeSession(None, inputString, gameTime, None, None)

	if inputString != 'exit':
		checkSession()

def inputEnd(rowId):
	choice = ''
	while choice != 'close' and  choice != 'delete' and choice != 'input':
		choice = input('Options: close, delete, input\n')
	endTime = tf.roundTime(dt.datetime.now())
	endTime = tf.removeSeconds(endTime)

	if choice == 'close':
		dataops.closeSession(endTime)
		checkSession()
	elif choice == 'delete':
		deleteSession(rowId)
	elif choice == 'input':
		userInputEndTime()

def userInputEndTime():
	inputCorrect = False
	while inputCorrect == False:
		userEndTime = input('Enter end time in format: YYYY-MM-DD HH:MM:SS\n')
		isThisRightString = 'Entered time is: ' + userEndTime + '. Is this satisfactory? (y/n)'
		isThisRight = input(isThisRightString)
		if isThisRight == 'y':
			inputCorrect = True

	userEndTime = userEndTime.rstrip()
	userEndTime = tf.stringToDatetime(userEndTime)
	userEndTime = tf.roundTime(userEndTime)
	endTime = tf.removeSeconds(userEndTime)
	dataops.closeSession(endTime)
	checkSession()

def calculateDuration(rowId):
	times = dataops.returnTimes(rowId)
	startTime = times[0]['startTime']
	endTime = times[0]['endTime']
	startTime = tf.stringToDatetime(startTime)
	endTime = tf.stringToDatetime(endTime)
	duration = str(endTime - startTime)
	dataops.writeDuration(rowId, duration)

def listSessions(rowIds = None):
	if rowIds == None:
		rows = dataops.returnDatabaseContents()
		if len(rows) == 0:
			print('No sessions found in database')
		if len(rows) > 0:
			for row in rows:
				outString = rowString(row)
				print(outString)
	else:
		rows = []
		for rowId in rowIds:
			rows.append(dataops.returnRow(rowId))

		for row in rows:
			outString = rowString(row[0])	#Each row returned is a list, of which the elements are the rows
			print(outString)

def rowString(row):
	rowId = 'id: ' + str(row['id'])
	name = 'name: ' + str(row['name'])
	startTime = 'start: ' + str(row['startTime'])
	endTime = 'end: ' + str(row['endTime'])
	duration = 'duration: ' + str(row['duration'])
	rowString = ''
	listOfElements = [rowId, name, startTime, endTime, duration]
	for element in listOfElements:
		rowString = rowString + element + '	'

	return rowString

#Checks for cancel in every input prior to proceeding, can select session via id and edit name and times
def editSession():
	rowId = input('Enter id of session to be modified: ')
	#If not cancel, proceed with rest of function
	if rowId != 'cancel':
		listSessions(rowId)
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
			
				dataops.modifySession(rowId, key, value)

			if key == 'startTime' or key == 'endTime':
				calculateDuration(rowId)

			print('Edited session now is:')
			listSessions(rowId)

#If rowId is none, user input is taken. If it is not none, specified row is deleted
def deleteSession(rowId = None):
	if rowId == None:
		rowIdRaw = input('Enter ids to delete: ')
		if rowIdRaw != 'cancel':
			rowIds = rowIdRaw.split()
			print('The following sessions will be deleted: ')
			listSessions(rowIds)
			proceed = input('Proceed? (y/n)')
			if proceed == 'y':
				for rowId in rowIds:
					dataops.deleteSession(int(rowId))
	else:
		dataops.deleteSession(rowId)

	checkSession()

checkSession()

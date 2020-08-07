import datetime as dt
import calendar
import databaseOperations as dataops
import timeFunctions

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
	gameTime = roundTime(dateAndTimeRaw)
	gameTime = removeSeconds(gameTime)

	if inputString == 'modify':
		listSessions()
		modify()
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
	endTime = roundTime(dt.datetime.now())
	endTime = removeSeconds(endTime)

	if choice == 'close':
		dataops.closeSession(endTime)
		checkSession()
	elif choice == 'delete':
		deleteSession(rowId)
	elif choice == 'input':
		userInputEndTime()

def deleteSession(rowId = None):
	if rowId == None:
		rowIdRaw = input('Enter ids to delete: ')
		rowIds = rowIdRaw.split()
		for rowId in rowIds:
			dataops.deleteSession(int(rowId))
	else:
		dataops.deleteSession(rowId)

	checkSession()

def userInputEndTime():
	inputCorrect = False
	while inputCorrect == False:
		userEndTime = input('Enter end time in format: YYYY-MM-DD HH:MM:SS\n')
		isThisRightString = 'Entered time is: ' + userEndTime + '. Is this satisfactory? (y/n)'
		isThisRight = input(isThisRightString)
		if isThisRight == 'y':
			inputCorrect = True

	userEndTime = userEndTime.rstrip()
	# userEndTime = dt.datetime.strptime(userEndTime, '%Y-%m-%d %H:%M:%S')
	userEndTime = stringToDatetime(userEndTime)
	userEndTime = roundTime(userEndTime)
	endTime = removeSeconds(userEndTime)
	dataops.closeSession(endTime)
	checkSession()

def calculateDuration(rowId):
	times = dataops.returnTimes(rowId)
	startTime = times[0]['startTime']
	endTime = times[0]['endTime']
	# startTime = dt.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S')
	# endTime = dt.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S')
	startTime = stringToDatetime(startTime)
	endTime = stringToDatetime(endTime)
	duration = str(endTime - startTime)
	# duration = dt.datetime.strftime(duration, '%H:%M:%S')
	dataops.writeDuration(rowId, duration)

def listSessions():
	rows = dataops.returnDatabaseContents()
	if len(rows) == 0:
		print('No sessions found in database')

	if len(rows) > 0:
		for row in rows:
			rowId = 'id: ' + str(row['id'])
			name = 'name: ' + str(row['name'])
			startTime = 'start: ' + str(row['startTime'])
			endTime = 'end: ' + str(row['endTime'])
			duration = 'duration: ' + str(row['duration'])
			outString = ''
			listOfElements = [rowId, name, startTime, endTime, duration]
			for element in listOfElements:
				outString = outString + element + '	'
			print(outString)

def modify():
	action = ''
	while action != 'delete' and action != 'modify' and action != 'cancel':
		action = input('Select action: delete, modify, cancel\n')
	if action == 'cancel':
		checkSession()

	if action == 'delete':
		deleteSession()

	if action == 'modify':
		modifySession()

def modifySession():
	listSessions()
	rowId = input('Enter id of session to be modified: ')
	validKey = False
	keys = ['name', 'startTime', 'endTime']
	while validKey == False:
		key = input('Enter key (name, startTime, endTime): ')
		if keys.count(key) == 1:
			validKey = True

	value = input('Enter new value: ')

	if key == 'startTime' or key == 'endTime':
		value = roundTime(value)
		value = removeSeconds(value)

	dataops.modifySession(rowId, key, value)

	if key == 'startTime' or key == 'endTime':
		calculateDuration(rowId)

#Returns number of days in requested month
def daysInMonth(dateAndTime):
	year = dateAndTime['year']
	month = dateAndTime['month']

	days = calendar.monthrange(year, month)[1]
	return days

#Rounds time to nearest minute, second is not used elsewhere in code
def roundTime(dateAndTimeRaw):
	inputType = str(type(dateAndTimeRaw))
	if 'str' in inputType:
		dateAndTimeRaw = stringToDatetime(dateAndTimeRaw)

	if dateAndTimeRaw.second >= 30:
		oneMinute = dt.timedelta(minutes = 1)
		dateAndTimeRaw = dateAndTimeRaw + oneMinute

	return dateAndTimeRaw

#Gets rid of the seconds part of time, as second level accuracy is not used
def removeSeconds(gameTime):
	second = gameTime.second
	microsecond = gameTime.microsecond
	secondValues = dt.timedelta(seconds = second, microseconds = microsecond)
	gameTime = gameTime - secondValues

	return gameTime

def stringToDatetime(dateTimeString):
	dateTime = dt.datetime.strptime(dateTimeString, '%Y-%m-%d %H:%M:%S')

	return dateTime

checkSession()

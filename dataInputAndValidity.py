import databaseOperations as dataops
import timeFunctions as tf


# Takes inputs starting with '/', and splits it into command and args. Arguments must be comma seperated
def processCommand(inputString):
	inputString = inputString.lstrip('/')
	inputString = inputString.strip()

	command, *arguments = inputString.split(' ', 1)
	if len(arguments) == 0:
		arguments = None
	elif len(arguments) != 0:
		arguments = arguments[0]
		arguments = arguments.split(',')

		for i in range(len(arguments)):
			arguments[i] = arguments[i].strip()

	return command, arguments


# Takes user input for rowId, checks if it is int, and exists in db, then returns it
def rowIdInput(inputString, multipleRowIds):
	validRowId = False
	while validRowId is False:
		checks = []
		# Takes input
		rowIdList = input(inputString)
		rowIdList = rowIdList.split(',')
		for i in range(len(rowIdList)):
			rowIdList[i] = rowIdList[i].strip()

		# Exit
		if '/cancel' in rowIdList:
			break

		# Series of checks for data to pass
		validRowIdCount = checkRowIdCount(rowIdList, multipleRowIds)
		checks.append(validRowIdCount)
		if validRowIdCount:
			validRowIdType = checkRowIdType(rowIdList)
			checks.append(validRowIdType)
			if validRowIdType:
				rowIdExist = checkRowIdExist(rowIdList)
				checks.append(rowIdExist)

		# If the above checks pass, exit loop
		if False not in checks:
			validRowId = True

	return rowIdList


# Checks if too many rowIds are given
def checkRowIdCount(rowIdList, multipleRowIds):
	validRowIdCount = True
	if len(rowIdList) > 1 and multipleRowIds is False:
		print('Too many inputs')
		validRowIdCount = False

	return validRowIdCount


# Checks if rowIds can be converted to int
def checkRowIdType(rowIdList):
	validRowIdType = True
	for rowId in rowIdList:
		try:
			_ = int(rowId)
		except Exception:
			print('id must be an integer')
			validRowIdType = False
			break

	return validRowIdType


# Checks if rowIds exist
def checkRowIdExist(rowIdList):
	presentRowIds = []
	rows = dataops.returnDatabaseContents()
	for row in rows:
		rowId = row['id']
		presentRowIds.append(str(rowId))

	absentRowIds = []
	rowIdExist = True
	for rowId in rowIdList:
		if rowId not in presentRowIds:
			rowIdExist = False
			absentRowIds.append(rowId)

	if rowIdExist is False:
		absentRowIdString = 'The following ids do not exist:'
		for rowId in absentRowIds:
			absentRowIdString = absentRowIdString + ' ' + str(rowId)
		print(absentRowIdString)

	return rowIdExist


# Takes user input for key, checks if it exists in provided list, then returns it
def keyInput(keyList, inputString):
	if inputString is None:
		inputString = generateKeyInputString(keyList)

	validKey = False
	while validKey is False:
		key = input(inputString)
		key = key.strip()
		if key in keyList:
			validKey = True
		elif key == '/cancel':
			validKey = True

	return key


# Generates string for use in input() if no string is provided
def generateKeyInputString(keyList):
	inputString = 'Enter key ('
	for key in keyList:
		inputString = inputString + str(key) + ' '
	inputString = inputString.rstrip()
	inputString = inputString + '): '

	return inputString


# Takes yes/no inputs
def ynChoiceInput(inputString):
	validChoice = False
	while validChoice is False:
		choice = input(inputString + ' (y/n): ')
		if choice in ['y', 'n']:
			validChoice = True

	if choice == 'y':
		return True
	elif choice == 'n':
		return False


# Takes user input for names (or commands, as both are entered in the same location)
def nameInput(inputString):
	nameString = input(inputString)
	nameString = nameString.strip()

	return nameString


# Takes user input for any time, checks if it is of the right format, checks if resulting duration > 0, then returns it
def timeInput(rowId, inputString, startOrEnd):
	validDateTime = False
	while validDateTime is False:
		checks = []
		dateTimeString = input(inputString)
		dateTimeString = dateTimeString.strip()

		if dateTimeString == '/cancel':
			break

		validDateTimeFormat = checkDateTimeFormat(dateTimeString)
		checks.append(validDateTimeFormat)
		if validDateTimeFormat:
			dateTime = tf.processDateTimeString(dateTimeString)
			if rowId is not None:
				validTimeDifference = checkTimeDifference(rowId, dateTime, startOrEnd)
				checks.append(validTimeDifference)

		if False not in checks:
			dateTimeString = tf.datetimeToString(dateTime, backup=False)
			validDateTime = True

	return dateTimeString


# Checks format of input by attempting to run strptime
def checkDateTimeFormat(dateTimeString):
	validDateTimeFormat = True
	try:
		_ = tf.stringToDatetime(dateTimeString)
	except Exception as e:
		print('Wrong format entered')
		print(e)
		validDateTimeFormat = False

	return validDateTimeFormat


# Checks if datetime.timedelta.days < 0
def checkTimeDifference(rowId, dateTime, startOrEnd):
	validTimeDifference = True
	times = dataops.returnTimes(rowId)[0]

	if startOrEnd == 'startTime':
		startTime = dateTime
		endTime = tf.stringToDatetime(times['endTime'])

	if startOrEnd == 'endTime':
		startTime = tf.stringToDatetime(times['startTime'])
		endTime = dateTime

	delta = endTime - startTime

	if delta.days < 0:
		print('Duration is negative')
		validTimeDifference = False

	return validTimeDifference


def durationInput():
	pass


def changeDurationStringFormat(rows, cols):
	for i in range(len(rows)):
		rows[i] = dict(rows[i])

		for col in cols:
			if rows[i][col] is not None:
				split = rows[i][col].split(':')

				# Formatting to hh:mm
				# for j in range(2):
				# 	if len(split[j]) == 1:
				# 		split[j] = '0' + split[j]

				# Formatting to h:mm
				if int(split[0]) < 10:
					split[0] = str(int(split[0]))
				if len(split[1]) == 1:
					split[1] = '0' + split[1]

				rows[i][col] = split[0] + ':' + split[1]

	return rows

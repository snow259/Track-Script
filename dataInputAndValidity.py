import databaseOperations as dataops
import timeFunctions as tf

#Takes inputs starting with '/', and splits it into command and args. Arguments must be comma seperated
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

#Takes user input for rowId, checks if it is int, and exists in db, then returns it
def rowIdInput(inputString, multipleRowIds):
	validRowId = False
	while validRowId == False:
		checks = []
		#Takes input
		rowIdList = input(inputString)
		rowIdList = rowIdList.strip()
		rowIdList = rowIdList.split()

		#Exit
		if '/cancel' in rowIdList:
			break
		
		validRowIdCount = checkRowIdCount(rowIdList, multipleRowIds)
		checks.append(validRowIdCount)
		if validRowIdCount == True:
			validRowIdType = checkRowIdType(rowIdList)
			checks.append(validRowIdType)
			if validRowIdType == True:
				rowIdExist = checkRowIdExist(rowIdList)
				checks.append(rowIdExist)

		#If the above checks pass, exit loop
		if False not in checks:
			validRowId = True

	return rowIdList

#Checks if too many rowIds are given
def checkRowIdCount(rowIdList, multipleRowIds):
		validRowIdCount = True
		if len(rowIdList) > 1 and multipleRowIds == False:
			print('Too many inputs')
			validRowIdCount = False

		return validRowIdCount

#Checks if rowIds can be converted to int
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

#Checks if rowIds exist
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

	if rowIdExist == False:
		absentRowIdString = 'The following ids do not exist:'
		for rowId in absentRowIds:
			absentRowIdString = absentRowIdString + ' ' + str(rowId)
		print(absentRowIdString)

	return rowIdExist

#Takes user input for key, checks if it exists in provided list, then returns it
def keyInput(keyList, inputString):
	if inputString == None:
		inputString = generateKeyInputString(keyList)

	validKey = False
	while validKey == False:
		key = input(inputString)
		if key in keyList:
			validKey = True
		elif key == '/cancel':
			validKey = True

	return key

#Generates string for use in input() if no string is provided
def generateKeyInputString(keyList):
	inputString = 'Enter key ('
	for key in keyList:
		inputString = inputString + str(key) + ' '
	inputString = inputString.rstrip()
	inputString = inputString + '): '

	return inputString

#Takes yes/no inputs
def ynChoiceInput(inputString):
	validChoice = False
	while validChoice == False:
		choice = input(inputString + ' (y/n): ')
		if choice in ['y', 'n']:
			validChoice = True

	if choice == 'y':
		return True
	elif choice == 'n':
		return False

def nameInput():
	pass

#Takes user input for any time, checks if it is of the right format, checks if resulting duration > 0, then returns it
def timeInput(rowId, inputString, startOrEnd):
	validDateTime = False
	while validDateTime == False:
		checks = []
		dateTimeString = input(inputString)
		dateTimeString = dateTimeString.strip()

		if dateTimeString == '/cancel':
			break

		validDateTimeFormat = checkDateTimeFormat(dateTimeString)
		checks.append(validDateTimeFormat)
		if validDateTimeFormat == True:
			dateTime = tf.processDateTimeString(dateTimeString)
			if rowId != None:
				validTimeDifference = checkTimeDifference(rowId, dateTime, startOrEnd)
				checks.append(validTimeDifference)

		if False not in checks:
			dateTimeString = tf.datetimeToString(dateTime, backup = False)
			validDateTime = True

	return dateTimeString

#Checks format of input by attempting to run strptime
def checkDateTimeFormat(dateTimeString):
	validDateTimeFormat = True
	try:
		_ = tf.stringToDatetime(dateTimeString)
	except Exception as e:
		print('Wrong format entered')
		print(e)
		validDateTimeFormat = False

	return validDateTimeFormat

#Checks if datetime.timedelta.days < 0
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
	
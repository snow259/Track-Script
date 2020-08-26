import databaseOperations as dataops
import timeFunctions as tf

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

def nameInput():
	pass

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

def checkDateTimeFormat(dateTimeString):
	validDateTimeFormat = True
	try:
		_ = tf.stringToDatetime(dateTimeString)
	except Exception as e:
		print('Wrong format entered')
		print(e)
		validDateTimeFormat = False

	return validDateTimeFormat

def checkTimeDifference(rowId, dateTime, startOrEnd):
	validTimeDifference = True
	times = dataops.returnTimes(rowId)

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
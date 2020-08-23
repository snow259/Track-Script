import databaseOperations as dataops

def rowIdInput(inputString, multipleRowIds):
	validRowId = False
	while validRowId == False:
		#Takes input
		rowIdList = input(inputString)
		rowIdList = rowIdList.split()

		if '/cancel' in rowIdList:
			break
		#Checks if too many rowIds are given. If not, checks if all can be int
		validRowIdCount = True
		if len(rowIdList) > 1 and multipleRowIds == False:
			print('Too many inputs')
			validRowIdCount = False
			
		validRowIdType = checkRowIdType(rowIdList)
		rowIdExist = checkRowIdExist(rowIdList)

		#If the above two checks pass, exit loop
		if validRowIdType == True and validRowIdCount == True and rowIdExist == True:
			validRowId = True

	return rowIdList

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

def timeInput():
	pass

def durationInput():
	pass
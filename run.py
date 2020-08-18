import track

backupInterval = 5	#Value is in days

#If openSessions == 0, compute durations if missing, backup if enough days has passed, then take input
def noOpenSessions():
	track.checkDuration()
	track.backup(backupInterval)
	inputString, gameTime = track.userInput()

	if inputString == 'edit':
		track.listSessions()
		track.editSession()
	elif inputString == 'delete':
		track.listSessions()
		track.deleteSession()
		track.listSessions()
	elif inputString == 'list':
		track.listSessions()
	elif inputString == 'backup':
		track.runBackupOperations()
		track.listSessions()
	elif inputString == 'exit':
		loop[0] = False
	else:
		track.writeStart(inputString, gameTime)

#If openSessions == 1, take input to close it
def oneOpenSession(rows):
	rowId = rows[0]['id']
	row = rows[0]
	track.printOpenSession(row)
	track.inputEnd(rowId)
	track.checkDuration()
	track.listSpecificSessions([rowId])

#If openSessions > 1, take input for repair choice, then repair
def manyOpenSessions(rows):
	repairOption = track.multipleSessionRepairChoice(rows)

	if repairOption == 'close':
		rowId = input('Enter id of session to close:\n')
		track.userInputEndTime(rowId)
	elif repairOption == 'delete':
		deleteSession()

if __name__ == '__main__':
	loop = [True]	#Editable from within functions
	track.listSessions()
	while loop[0] == True:
		rows = track.checkSession()
		openSessions = len(rows)
		
		if openSessions == 0:
			noOpenSessions()
		elif openSessions == 1:
			oneOpenSession(rows)
		elif openSessions > 1:
			manyOpenSessions(rows)

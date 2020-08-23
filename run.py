import track
import dataInputAndValidity as di

backupInterval = 5	#Value is in days
userDeclinedBackup = [False]	#Editable within function
#Checks if backup is required, then asks user if backup can be performed
def backup():
	#Checks if user wants to perform backup before performing it. Does not ask user to backup until reopening script if declined
	mustBackup = track.backup(backupInterval)
	if mustBackup == True and userDeclinedBackup[0] == False:
		userBackupChoice = input('It has been more than ' + str(backupInterval) + ' days since last backup. Run backup? (y/n)\n')
		if userBackupChoice == 'y':
			runBackup()
		else:
			userDeclinedBackup[0] = True

#If user agrees to backup, backup is attempted
def runBackup():
	try:
		track.runBackupOperations()
	except Exception as e:
		print('Possible issue with backup')
		print(e)
	else:
		print('Backup successfully completed')
		track.listSessions()

#If openSessions == 0, compute durations if missing, then take input
def noOpenSessions():
	track.checkDuration()

	inputString, gameTime = track.userInput()

	if inputString.startswith('/'):
		command = inputString.lstrip('/')
		if command == 'edit':
			track.listSessions()
			track.editSession()
		elif command == 'delete':
			track.listSessions()
			track.deleteSession()
			track.listSessions()
		elif command == 'list':
			track.listSessions()
		elif command == 'backup':
			runBackup()
		elif command == 'exit':
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
		rowId = di.rowIdInput('Enter id of session to close\n', multipleRowIds = False)
		track.userInputEndTime(rowId)
	elif repairOption == 'delete':
		track.deleteSession()

if __name__ == '__main__':
	loop = [True]	#Editable from within functions
	track.listSessions()
	while loop[0] == True:
		rows = track.checkSession()
		openSessions = len(rows)
		
		if openSessions == 0:
			backup()
			noOpenSessions()
		elif openSessions == 1:
			oneOpenSession(rows)
		elif openSessions > 1:
			manyOpenSessions(rows)

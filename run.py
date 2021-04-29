import track
import commands as cmd
import dataInputAndValidity as di
import gameLife as gl
import output as op

backupInterval = 5	#Value is in days
userDeclinedBackup = [False]	#Editable within function
#Checks if backup is required, then asks user if backup can be performed
def backup():
	#Checks if user wants to perform backup before performing it. Does not ask user to backup until reopening script if declined
	mustBackup = track.backup(backupInterval)
	if mustBackup == True and userDeclinedBackup[0] == False:
		userBackupChoice = di.ynChoiceInput('It has been more than ' + str(backupInterval) + ' days since last backup. Run backup?')
		if userBackupChoice:
			runBackup()
		else:
			print('Backup deferred')
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
		command, argument = di.processCommand(inputString)
		if command == 'edit':
			cmd.editCommand(argument)
		elif command == 'delete':
			cmd.deleteCommand(argument)
		elif command == 'list':
			cmd.listCommand(argument)
		elif command == 'backup':
			runBackup()
		elif command == 'random':
			cmd.randomCommand(argument)
		elif command == 'gamelife':
			cmd.gamelifeCommand(argument)
		elif command == 'exit':
			loop[0] = False
	elif len(inputString) == 0:
		#Stripped blank inputs have length 0
		pass
	else:
		track.writeStart(inputString, gameTime)

#If openSessions == 1, take input to close it
def oneOpenSession(rows):
	rowId = rows[0]['id']
	name = rows[0]['name']

	print('Open session: ')
	op.printOutput(rows)
	choice = track.inputEnd(rowId)
	track.checkDuration()
	track.listSpecificSessions([rowId])

	#If session is closed in any manner, lastPlayed is updated
	if choice == 'close' or choice == 'input':
		gl.checkLife(name)

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

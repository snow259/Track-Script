import track
import dataInputAndValidity as di
import randomChoice as rc
import gameLife as gl
#All command related functions were split off here due to growing complexity caused by gameLife

def editCommand(argument):
	rowsBeforeEdit = track.listSessions()

	if rowsBeforeEdit == None:
		print('Nothing to edit')
	else:
		editDetails = track.editSession()

		if editDetails != None:
			rowId, key, value = editDetails

			print('Edited session now is:')
			_ = listSpecificSessions([rowId])[0]	#List containing rows

			editDetails = {'id': rowId, key: value}
			if key == 'startTime' or key == 'endTime':
				gl.updateLifeEdited(rowsBeforeEdit, editDetails)

def deleteCommand(argument):
	track.listSessions()
	track.deleteSession()
	track.listSessions()

def listCommand(argument):
	track.listSessions()

def backupCommand(argument):
	runBackup()

def randomCommand(argument):
	rc.randomGame(argument)

def gamelifeCommand(argument):
	gl.populateGameLife()

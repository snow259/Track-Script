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
			_ = track.listSpecificSessions([rowId])[0]	#List containing rows

			#If name is edited, check life of new name
			if key == 'name':
				gl.checkLife(value)

			#Check life of original name, regardless of if name was edited
			for row in rowsBeforeEdit:
				if row['id'] == int(rowId):
					gl.checkLife(row['name'])
					break

def deleteCommand(argument):
	rowsBeforeDelete = track.listSessions()
	rowIds = track.deleteSession()
	rowsAfterDelete = track.listSessions()

	if rowIds != None:
		for row in rowsBeforeDelete:
			if row['id'] in rowIds:
				gl.checkLife(row['name'])

def listCommand(argument):
	track.listSessions()

def randomCommand(argument):
	rc.randomGame(argument)

def gamelifeCommand(argument):
	pass

import track
import randomChoice as rc
import databaseOperations as dataops
import output as op
import gameLife as gl
import gameStatistics as gs
# All command related functions were split off here due to growing complexity caused by gameLife


def editCommand(argument):
	rowsBeforeEdit = track.listSessions()

	if rowsBeforeEdit is None:
		print('Nothing to edit')
	else:
		editDetails = track.editSession()

		if editDetails is not None:
			rowId, key, value = editDetails
			print('Edited session now is:')
			_ = track.listSpecificSessions([rowId])[0]		# List containing rows

			# If name is edited, check life of new name
			if key == 'name':
				gl.checkLife(value)

			# Check life of original name, regardless of if name was edited
			for row in rowsBeforeEdit:
				if row['id'] == int(rowId):
					gl.checkLife(row['name'])
					break


def deleteCommand(argument):
	rowsBeforeDelete = track.listSessions()
	rowIds = track.deleteSession()

	if rowIds is not None:
		for row in rowsBeforeDelete:
			if row['id'] in rowIds:
				gl.checkLife(row['name'])


def listCommand(argument):
	track.listSessions()


def randomCommand(argument):
	rc.randomGame(argument)


# Prints out the last numberOfRecentGames games played
def recentCommand(argument):
	# Defaults to last 5 if no argument is provided or if argument cannot be converted to int
	if argument is None:
		numberOfRecentGames = 5
	else:
		try:
			numberOfRecentGames = int(argument[0])
		except ValueError:
			print('Invalid integer, using defaults')
			numberOfRecentGames = 5

	gameLifeSorted = dataops.returnGameLifeSorted()

	# If there aren't enough games played, print all games played in order
	if numberOfRecentGames > len(gameLifeSorted):
		numberOfRecentGames = len(gameLifeSorted)

	# If there are no games in list, state that. Else, print as usual
	if numberOfRecentGames == 0:
		print('\nNo recently played games found in database')
	else:
		print('\nLast ' + str(numberOfRecentGames) + ' games played:')

		op.printOutput(gameLifeSorted[:numberOfRecentGames])


# Prints out the life of game x where x is argument
def gamelifeCommand(argument):
	pass


# Prints out the top n games played where n is an argument
def topPlayedCommand(argument):
	rows = dataops.returnTotalTimePlayed()

	if argument is not None:
		try:
			argument = int(argument[0])
		except ValueError:
			argument = 10
	else:
		argument = 10

	gs.topPlayed(argument, rows)

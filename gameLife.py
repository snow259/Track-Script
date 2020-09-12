import databaseOperations as dataops
import timeFunctions as tf

#Checks if table GameLife exists. Creates it if it doesn't. This is done on import
def checkForTables():
	tables = dataops.returnTablesList()

	if 'GameLife' not in tables:
		dataops.createGameLifeTable()
		populateGameLife()

#If table was just created, function fills it with all existing game lives.
def populateGameLife():
	mainDatabaseRows = dataops.returnDatabaseContents()
	archiveRows = dataops.returnArchiveContents()

	life = {}
	life = populateNames(life, mainDatabaseRows)
	life = populateNames(life, archiveRows)

	life = findAllLife(life, mainDatabaseRows)
	life = findAllLife(life, archiveRows)

	writeNewLife(life)

#Finds all game names from provided rows and appends them to the life dictionary if it is not found in it
def populateNames(life, rows):
	for row in rows:
		name = row['name']
		if name not in life:
			life[name] = {'firstPlayed': None, 'lastPlayed': None}

	return life

#Writes all game life to table.
#TODO: reuse function for updating
def writeNewLife(life):
	for game in life:
		name = game
		firstPlayed = life[game]['firstPlayed']
		lastPlayed = life[game]['lastPlayed']
		dataops.addGameToGameLifeTable(name, firstPlayed, lastPlayed)

#Replaces None with datetime, if not none replaces lastPlayedTime with endTime if endTime is more recent
#dateime > datetime implies the numbers in the first datetime are larger, which will be due to it being more recent
def findAllLife(life, rows):
	for row in rows:
		name = row['name']
		startTime = row['startTime']
		endTime = row['endTime']

		startTime = tf.stringToDatetime(startTime)
		endTime = tf.stringToDatetime(endTime)

		for gameName in life:
			if gameName == name:
				lastPlayedTime = life[gameName]['lastPlayed']
				firstPlayedTime = life[gameName]['firstPlayed']

				if lastPlayedTime == None:
					life[gameName]['lastPlayed'] = endTime
				else:
					if endTime > lastPlayedTime:
						life[gameName]['lastPlayed'] = endTime

				if firstPlayedTime == None:
					life[gameName]['firstPlayed'] = startTime
				else:
					if startTime < firstPlayedTime:
						life[gameName]['firstPlayed'] = startTime

	return life

def updateLifeClosed(openSession, endTime):
	life = dataops.returnGameLife()
	life = convertLifeRows(life)
	name = openSession['name']
	startTime = openSession['startTime']

	if name not in life:
		newLife = {name: {'firstPlayed': startTime, 'lastPlayed': endTime}}
		writeNewLife(newLife)
	else:
		originalLastPlayed = life[name]['lastPlayed']
		originalLastPlayed = tf.stringToDatetime(originalLastPlayed)

		if originalLastPlayed < endTime:
			dataops.updateGameLife(name, 'lastPlayed', endTime)

#Updates the life of games within the dictionary
def updateLifeEdited(rowsBeforeEdit, editDetails):
	life = dataops.returnGameLife()
	life = convertLifeRows(life)

	rowId = editDetails['id']
	originalSession = findOriginalSession(rowsBeforeEdit, rowId)

	name = originalSession['name']

	firstPlayed = life[name]['firstPlayed']
	firstPlayed = tf.stringToDatetime(firstPlayed)
	lastPlayed = life[name]['lastPlayed']
	lastPlayed = tf.stringToDatetime(lastPlayed)

	originalStartTime = originalSession['startTime']
	originalStartTime = tf.stringToDatetime(originalStartTime)
	originalEndTime = originalSession['endTime']
	originalEndTime = tf.stringToDatetime(originalEndTime)

	lifeToEdit = {}
	if 'startTime' in editDetails:
		if originalStartTime == firstPlayed:
			lifeToEdit[name] = 'both'
	elif 'endTime' in editDetails:
		if originalEndTime == lastPlayed:
			lifeToEdit[name] = 'both'
	elif 'name' in editDetails:
		pass

	if len(lifeToEdit) > 0:
		newLife = findNewLife(life, lifeToEdit)
		for name in newLife:
			key = lifeToEdit[name]
			if key == 'both':
				firstPlayed = newLife[name]['firstPlayed']
				lastPlayed = newLife[name]['lastPlayed']
				dataops.updateGameLife(name, 'firstPlayed', firstPlayed)
				dataops.updateGameLife(name, 'lastPlayed', lastPlayed)

def updateLifeDeleted(rowsBeforeDelete, rowIds):
	life = dataops.returnGameLife()
	life = convertLifeRows(life)

	deletedRows = []
	for rowId in rowIds:
		deletedRow = findOriginalSession(rowsBeforeDelete, rowId)
		deletedRows.append(deletedRow)

	lifeToEdit = {}
	for row in deletedRows:
		name = row['name']
		for gameLifeName in life:
			if gameLifeName == name:
				firstPlayed = life[gameLifeName]['firstPlayed']
				lastPlayed = life[gameLifeName]['lastPlayed']
				startTime = row['startTime']
				endTime = row['endTime']

				if firstPlayed == startTime and lastPlayed == endTime:
					dataops.deleteGameLife(name)
				elif firstPlayed == startTime:
					lifeToEdit[name] = 'both'
				elif lastPlayed == endTime:
					lifeToEdit[name] = 'both'

	if len(lifeToEdit) > 0:
		newLife = findNewLife(life, lifeToEdit)
		for name in newLife:
			key = lifeToEdit[name]
			if key == 'both':
				firstPlayed = newLife[name]['firstPlayed']
				lastPlayed = newLife[name]['lastPlayed']
				dataops.updateGameLife(name, 'firstPlayed', firstPlayed)
				dataops.updateGameLife(name, 'lastPlayed', lastPlayed)

#Finds updated life of game
def findNewLife(life, lifeToEdit):
	mainDatabaseRows = dataops.returnDatabaseContents()
	archiveRows = dataops.returnArchiveContents()

	#Filling life with known values
	newLife = {}
	for name in lifeToEdit:
		if lifeToEdit[name] == 'firstPlayed':
			lastPlayed = life[name]['lastPlayed']
			newLife[name] = {'firstPlayed': None, 'lastPlayed': lastPlayed}
		elif lifeToEdit[name] == 'lastPlayed':
			firstPlayed = life[name]['firstPlayed']
			newLife[name] = {'firstPlayed': firstPlayed, 'lastPlayed': None}
		elif lifeToEdit[name] == 'both':
			newLife[name] = {'firstPlayed': None, 'lastPlayed': None}

	newLife = findAllLife(newLife, mainDatabaseRows)
	newLife = findAllLife(newLife, archiveRows)

	return newLife

#Converts life from sqlite3.Row objects to dictionary
def convertLifeRows(life):
	convertedLife = {}
	for i in range(len(life)):
		row = life[i]
		name = row['name']
		firstPlayed = row['firstPlayed']
		lastPlayed = row['lastPlayed']

		convertedLife[name] = {'firstPlayed': firstPlayed, 'lastPlayed': lastPlayed}

	return convertedLife

def findOriginalSession(rowsBeforeEvent, rowId):
	for row in rowsBeforeEvent:

		if row['id'] == int(rowId):
			name = row['name']
			startTime = row['startTime']
			endTime = row['endTime']
			duration = row['duration']
			originalSession = {'id': rowId, 'name': name, 'startTime': startTime, 'endTime': endTime, 'duration': duration}

			return originalSession

def findLife(name):
	pass

checkForTables()

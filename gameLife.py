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

	life = findLife(life, mainDatabaseRows)
	life = findLife(life, archiveRows)

	writeNewLife(life)

#Finds all game names from provided rows and appends them to the life dictionary if it is not found in it
def populateNames(life, rows):
	for row in rows:
		name = row['name']
		if name not in life:
			life[name] = {'firstPlayed': None, 'lastPlayed': None}

	return life

#Replaces None with datetime, if not none replaces lastPlayedTime with endTime if endTime is more recent
#dateime > datetime implies the numbers in the first datetime are larger, which will be due to it being more recent
def findLife(life, rows):
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

#Writes all game life to table.
#TODO: reuse function for updating
def writeNewLife(life):
	for game in life:
		name = game
		firstPlayed = life[game]['firstPlayed']
		lastPlayed = life[game]['lastPlayed']
		dataops.addGameToGameLifeTable(name, firstPlayed, lastPlayed)

#Converts life from sqlite3.Row objects to dictionary
def convertLifeRows(life):
	convertedLife = {}
	for i in range(len(life)):
		row = life[i]
		name = row['name']
		firstPlayed = tf.stringToDatetime(row['firstPlayed'])
		lastPlayed = tf.stringToDatetime(row['lastPlayed'])

		convertedLife[name] = {'firstPlayed': firstPlayed, 'lastPlayed': lastPlayed}

	return convertedLife

def checkLife(name):
	life = dataops.returnGameLife()
	life = convertLifeRows(life)

	gameRowsMain = dataops.returnGameMain(name)
	gameRowsArchive = dataops.returnGameArchive(name)

	#Checks if name is missing from sessions
	if len(gameRowsMain) == len(gameRowsArchive) == 0:
		dataops.deleteGameLife(name)

	#If present, updates life
	else:
		updatedLife = {}
		updatedLife[name] = {'firstPlayed': None, 'lastPlayed': None}

		updatedLife = findLife(updatedLife, gameRowsMain)
		updatedLife = findLife(updatedLife, gameRowsArchive)

		#Checks if name is a new game
		if name not in life:
			writeNewLife(updatedLife)

		#If not a new game
		else:
			firstPlayed = updatedLife[name]['firstPlayed']
			lastPlayed = updatedLife[name]['lastPlayed']
			dataops.updateGameLife(name, 'firstPlayed', firstPlayed)
			dataops.updateGameLife(name, 'lastPlayed', lastPlayed)

checkForTables()

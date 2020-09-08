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

#Updates the life of games within the dictionary
def updateLife(life):
	writeLife(life)

def findLife(name):
	pass

checkForTables()
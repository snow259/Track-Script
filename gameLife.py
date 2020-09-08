import databaseOperations as dataops
import timeFunctions as tf

def checkForTables():
	tables = dataops.returnTablesList()

	if 'GameLife' not in tables:
		dataops.createGameLifeTable()
		populateGameLife()

def populateGameLife():
	mainDatabaseRows = dataops.returnDatabaseContents()
	archiveRows = dataops.returnArchiveContents()

	life = {}
	life = populateNames(life, mainDatabaseRows)
	life = populateNames(life, archiveRows)

	life = findAllLife(life, mainDatabaseRows)
	life = findAllLife(life, archiveRows)

	writeLife(life)

def populateNames(life, rows):
	for row in rows:
		name = row['name']
		if name not in life:
			life[name] = {'firstPlayed': None, 'lastPlayed': None}

	return life

def writeLife(life):
	for game in life:
		name = game
		firstPlayed = life[game]['firstPlayed']
		lastPlayed = life[game]['lastPlayed']
		if firstPlayed == None and lastPlayed != None:
			key = 'lastPlayed'
			value = lastPlayed
			dataops.updateGameLife(name, key, value)
		elif firstPlayed != None and lastPlayed == None:
			key = 'firstPlayed'
			value = lastPlayed
			dataops.updateGameLife(name, key, value)
		else:
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

def updateLife(life):
	writeLife(life)

def findLife(name):
	pass

checkForTables()
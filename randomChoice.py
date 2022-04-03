import random
import databaseOperations as dataops


def randomGame(argument):
	# Prints new line before all other random choice outputs, none of which print new lines
	print('')

	if argument is None:
		randomChoice = randomRecentGame(5)
		print(randomChoice)
	else:
		argumentLength = len(argument)
		if argumentLength == 1:
			try:
				count = int(argument[0])
			except Exception:
				print('Too few arguments for random choice')
			else:
				if count > 1:
					randomChoice = randomRecentGame(count)
					print(randomChoice)
				else:
					print('Too few games for random choice')
		else:
			randomChoice = random.choice(argument)
			print(randomChoice)


# Pick game randomly from the last five games played
def randomRecentGame(count):
	gameLifeSorted = dataops.returnGameLifeSorted()

	if count > len(gameLifeSorted):
		print('Only ' + str(len(gameLifeSorted)) + ' games in database')
		count = len(gameLifeSorted)

	recentGames = []
	for i in range(count):
		recentGames.append(gameLifeSorted[i]['name'])

	randomChoice = random.choice(recentGames)

	return randomChoice

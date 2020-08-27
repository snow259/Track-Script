import random

def randomGame(argument):
	if argument == None:
		randomChoice = randomPastGame(5)
		print(randomChoice)
	else:
		argumentLength = len(argument)
		if argumentLength == 1:
			try:
				days = int(argument[0])
			except Exception:
				print('Too few arguments for random choice')
			else:
				randomChoice = randomPastGame(days)
				print(randomChoice)
		else:
			randomChoice = random.choice(argument)
			print(randomChoice)

#Pick game randomly from a game played in last five days
def randomPastGame(days):
	print(days)
	
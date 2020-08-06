import datetime as dt
import calendar
# import databaseOperations as dataops

# operatingDirectory = 

#Checks if database exists, creates it if it does not


#Takes input from user, reads current time
def inputGame():
	newGame = input('Enter game: ')
	# gameTime = stringDateTime(dt.datetime.now(), round = True)
	gameTime = roundTime(dt.datetime.now())
	gameTime = removeSeconds(gameTime)
	print(gameTime)

#Checks database for open session of game
# def checkSession():

#Writes game and time to database
# def writeToDB(game):

#Converts datetime object to dictionary, done to allow changing of values
def stringDateTime(dateAndTimeRaw, round):
	if round == True:
		dateAndTimeRaw = roundTime(dateAndTimeRaw)

	dateString = dt.date.isoformat(dateAndTimeRaw)
	timeString = dt.datetime.strftime(dateAndTimeRaw, '%H:%M:00')
	dateTimeString  = dateString + ' ' + timeString

	return dateTimeString

#Returns number of days in requested month
def daysInMonth(dateAndTime):
	year = dateAndTime['year']
	month = dateAndTime['month']

	days = calendar.monthrange(year, month)[1]
	return days

#Rounds time to nearest minute, second is not used elsewhere in code
def roundTime(dateAndTimeRaw):
	if dateAndTimeRaw.second >= 30:
		oneMinute = dt.timedelta(minutes = 1)
		dateAndTimeRaw = dateAndTimeRaw + oneMinute

	return dateAndTimeRaw

def removeSeconds(gameTime):
	second = gameTime.second
	microsecond = gameTime.microsecond
	secondValues = dt.timedelta(seconds = second, microseconds = microsecond)
	gameTime = gameTime - secondValues

	return gameTime

inputGame()

#Input game -> stuff to write thing to database
#			-> function to input end time of game, as only one game can be played at a time
#put input game in a while loop in __main__, with exit condition 
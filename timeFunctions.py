import datetime as dt
import calendar


# Returns number of days in requested month
def daysInMonth(dateAndTime):
	year = dateAndTime['year']
	month = dateAndTime['month']

	days = calendar.monthrange(year, month)[1]
	return days


# Rounds and removes seconds for datetime object
def processDateTime(dateTime):
	dateTime = roundTime(dateTime)
	dateTime = removeSeconds(dateTime)

	return dateTime


# Does the same as above but on a string input
def processDateTimeString(dateTimeString):
	dateTime = stringToDatetime(dateTimeString)
	dateTime = processDateTime(dateTime)

	return dateTime


# Rounds time to the nearest minute, second is not used elsewhere in code
def roundTime(dateAndTimeRaw):
	inputType = str(type(dateAndTimeRaw))
	if 'str' in inputType:
		dateAndTimeRaw = stringToDatetime(dateAndTimeRaw)

	if dateAndTimeRaw.second >= 30:
		oneMinute = dt.timedelta(minutes=1)
		dateAndTimeRaw = dateAndTimeRaw + oneMinute

	return dateAndTimeRaw


# Gets rid of the seconds part of time, as second level accuracy is not used
def removeSeconds(gameTime):
	second = gameTime.second
	microsecond = gameTime.microsecond
	secondValues = dt.timedelta(seconds=second, microseconds=microsecond)
	gameTime = gameTime - secondValues

	return gameTime


def stringToDatetime(dateTimeString):
	dateTime = dt.datetime.strptime(dateTimeString, '%Y-%m-%d %H:%M:%S')

	return dateTime


def datetimeToString(dateTime, backup=True):
	if backup is True:
		dateTimeString = dt.datetime.strftime(dateTime, '%Y%m%d%H%M%S')
	else:
		dateTimeString = dt.datetime.strftime(dateTime, '%Y-%m-%d %H:%M:%S')

	return dateTimeString


def dateToString(dateTime):
	dateString = dt.datetime.strftime(dateTime, '%Y-%m-%d')

	return dateString


def dateDifference(date1, dateTime):
	year = dateTime.year
	month = dateTime.month
	date = dateTime.day
	date2 = dt.date(year, month, date)

	difference = date1 - date2

	return difference


def stringToTimeDelta(timeDeltaString):
	timeDeltaString = timeDeltaString.split(':')

	return dt.timedelta(hours=int(timeDeltaString[0]), minutes=int(timeDeltaString[1]))


def timeDeltaToString(timeDelta, keepSeconds=False):
	seconds = int(timeDelta.seconds % 60)
	minutes = int(timeDelta.seconds / 60)
	hours = timeDelta.days * 24

	while minutes >= 60:
		hours += 1
		minutes -= 60

	seconds = str(seconds)
	minutes = str(minutes)
	hours = str(hours)

	# Convert string to ss from s
	if len(seconds) == 1:
		seconds = '0' + seconds

	# Convert string to mm from m
	if len(minutes) == 1:
		minutes = '0' + minutes

	# Convert string to hh from h
	# if len(hours) == 1:
	# 	hours = '0' + hours

	durationString = hours + ':' + minutes

	if keepSeconds is True:
		durationString = durationString + ':' + seconds

	return durationString

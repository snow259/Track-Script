import os
import csv
import datetime as dt
import databaseFunctions as dbf

filePath = os.path.realpath(__file__)
fileDirectory = os.path.dirname(filePath)
dirList = os.listdir(fileDirectory)

databaseName = 'legacyData.db'
databasePath = fileDirectory + '\\' + databaseName

titleRow = ['Month', 'Date', 'Day']
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

def findCsv():
	csvList = []
	for file in dirList:
		if file.endswith('session.csv'):
			csvList.append(file)

	csvList.sort()
	return csvList

def readCsv(file):
	with open(file) as dataFile:
		lines = []
		reader = csv.reader(dataFile)
		for row in reader:
			lines.append(row)

	return lines

#Removes title row, mentions of month, and all empty spaces by copying row into another variable, and not copying the stuff to be removed
def deleteExtraneous(lines):
	numberOfRows = len(lines)
	linesPruned = []

	for i in range(numberOfRows):
		row = lines[i]

		if row == titleRow:
			pass
		else:
			rowPruned = []
			for element in row:
				if element in months:
					pass
				elif element in days:
					pass
				elif element == '':
					pass
				else:
					rowPruned.append(element)
			linesPruned.append(rowPruned)

	return linesPruned

def writeLines(file, lines):
	for row in lines:
		date = row[0]
		rowLength = len(row)
		dateStamp = generateDateStamp(file, date)

		for i in range(1, rowLength):
			session = row[i]
			session = convertSession(dateStamp, session)
			dbf.writeSession(session)

def generateDateStamp(file, date):
	if len(date) == 1:
		date = '0' + date
	
	dateStamp = file.rstrip(' session.csv') + '-' + date

	return dateStamp

def convertSession(dateStamp, session):
	*nameSplit, startTimeRaw, _, endTimeRaw = session.split()

	name = joinName(nameSplit)
	startTime = generateTimeStamp(dateStamp, startTimeRaw)
	endTime = generateTimeStamp(dateStamp, endTimeRaw)
	duration = calculateDuration(startTime, endTime)

	session = {'name': name, 'startTime': startTime, 'endTime': endTime, 'duration': duration}

	return session

def joinName(nameSplit):
	name = ''
	for element in nameSplit:
		name = name + element + ' '
	name = name.strip()

	return name

def generateTimeStamp(dateStamp, time):
	hour, minute = time.split(':')
	second = '00'

	if len(hour) == 1:
		hour = '0' + hour
	if len(minute) == 1:
		minute = '0' + minute

	timeStamp = dateStamp + ' ' + hour + ':' + minute + ':' + second

	return timeStamp

def calculateDuration(startTime, endTime):
	startTime = stringToDateTime(startTime)
	endTime = stringToDateTime(endTime)

	duration = endTime - startTime
	duration = str(duration)

	return duration

def stringToDateTime(dateTimeString):
	dateTime = dt.datetime.strptime(dateTimeString, '%Y-%m-%d %H:%M:%S')

	return dateTime

def dateTimeToString(dateTime):
	dateTimeString = dt.datetime.strftime(dateTime, '%Y-%m-%d %H:%M:%S')

	return dateTimeString

def main():
	dbf.createDataBase()
	csvList = findCsv()

	for file in csvList:
		print('Writing: ' + str(file))
		writeStart = dt.datetime.now()
		lines = readCsv(file)
		lines = deleteExtraneous(lines)
		writeLines(file, lines)
		writeEnd = dt.datetime.now()
		writeDuration = writeEnd - writeStart
		print(str(file) + ' written in: ' + str(writeDuration))

if __name__ == '__main__':
	main()
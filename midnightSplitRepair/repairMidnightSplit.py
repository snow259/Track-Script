import os
import datetime as dt
import databaseOperations as dbf

def collectMidnightSessions():
	midnightEnd = dbf.returnMidnightEnd()
	midnightStart = dbf.returnMidnightStart()

	return midnightEnd, midnightStart

def printSessions(session):
	rowId = str(session['id'])
	name = str(session['name'])
	startTime = str(session['startTime'])
	endTime = str(session['endTime'])

	sessionString = 'id: ' + rowId + ' name: ' + name + ' startTime: ' + startTime + ' endTime: ' + endTime
	print(sessionString)

def findEnd(session, midnightStart):
	startTime = session['startTime']
	startTime = stringToDateTime(startTime)
	startDate = startTime.day
	startName = session['name']

	oneDay = dt.timedelta(days = 1)
	expectedEndDateTime = startTime + oneDay
	expectedEndDate = str(expectedEndDateTime.year) + str(expectedEndDateTime.month) + str(expectedEndDateTime.day)

	endSession = None
	for midnightSession in midnightStart:
		endDateTime = midnightSession['endTime']
		endDateTime = stringToDateTime(endDateTime)
		endMonth = endDateTime.month
		endDate = str(endDateTime.year) + str(endDateTime.month) + str(endDateTime.day)
		endName = midnightSession['name']

		if expectedEndDate == endDate:
			if startName == endName:
				endSession = midnightSession

	if endSession != None:
		return {'startSession': session, 'endSession': endSession}

def stringToDateTime(dateTimeString):
	dateTime = dt.datetime.strptime(dateTimeString, '%Y-%m-%d %H:%M:%S')

	return dateTime

def mergeSessions(sessionPairs):
	pass

def findUnpairedMidnightStart(midnightStart, sessionPairs):
	unpairedMidnightStart = []
	for session in midnightStart:
		rowId = session['id']
		paired = False
		for pair in sessionPairs:
			endSession = pair['endSession']
			endRowId = endSession['id']
			if rowId == endRowId:
				paired = True
				break

		if paired == False:
			unpairedMidnightStart.append(session)

	return unpairedMidnightStart

def printProcessedSessions(sessionPairs, unpairedMidnightEnd, unpairedMidnightStart):
	print('Session Pairs: ' + str(len(sessionPairs)))
	print('Unpaired Midnight End: ' + str(len(unpairedMidnightEnd)))
	print('Unpaired Midnight Start: ' + str(len(unpairedMidnightStart)))
	print('Session Pairs:')
	for sessionPair in sessionPairs:
		print('Pair:')
		printSessions(sessionPair['startSession'])
		printSessions(sessionPair['endSession'])
	print('Unpaired Midnight End')
	for session in unpairedMidnightEnd:
		printSessions(session)
	print('Unpaired Midnight Start')
	for session in unpairedMidnightStart:
		printSessions(session)

def main():
	midnightEnd, midnightStart = collectMidnightSessions()

	sessionPairs = []
	unpairedMidnightEnd = []
	for session in midnightEnd:
		sessionPair = findEnd(session, midnightStart)
		if sessionPair == None:
			unpairedMidnightEnd.append(session)
		else:
			sessionPairs.append(sessionPair)
	unpairedMidnightStart = findUnpairedMidnightStart(midnightStart, sessionPairs)

	mergedSessions = mergeSessions(sessionPairs)

if __name__ == '__main__':
	main()
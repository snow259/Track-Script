import os
import datetime as dt
import databaseOperations as dbf

#Collects both sessions that start at and end at midnight
def collectMidnightSessions():
	midnightEnd = dbf.returnMidnightEnd()
	midnightStart = dbf.returnMidnightStart()

	return midnightEnd, midnightStart

#Prints the sessions with key
def printSessions(session):
	rowId = str(session['id'])
	name = str(session['name'])
	startTime = str(session['startTime'])
	endTime = str(session['endTime'])

	sessionString = 'id: ' + rowId + ' name: ' + name + ' startTime: ' + startTime + ' endTime: ' + endTime
	print(sessionString)

#For a given session starting before midnight, this function looks for a corresponding session starting after midnight and returns the pair
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

#Takes all session pairs, and merges them into a single session. Also returns rowId of the second session for deletion
def mergeSessions(sessionPairs):
	mergedSessions = []
	deleteRowIds = []
	for sessionPair in sessionPairs:
		startSession = sessionPair['startSession']
		endSession = sessionPair['endSession']

		rowId = startSession['id']
		deleteRowId = endSession['id']

		startTime = startSession['startTime']
		startTime = stringToDateTime(startTime)

		endTime = endSession['endTime']
		endTime = stringToDateTime(endTime)

		duration = endTime - startTime

		mergedSession = {'id': rowId, 'startTime': startTime, 'endTime': endTime, 'duration': duration}

		mergedSessions.append(mergedSession)
		deleteRowIds.append(deleteRowId)

	return mergedSessions, deleteRowIds

#Looks for sessions that begin after midnight and do not have a corresponding session beginning before midnight
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

def updateDatabase(mergedSessions):
	for session in mergedSessions:
		dbf.modifySession(session)

def deleteSessions(deleteRowIds):
	for rowId in deleteRowIds:
		print(rowId)
		dbf.deleteSession(rowId)

#Just a print thing for debugging and to see how the data looks. Prints count and sessions of: pairs, unpaired before midnight, unpaired after midnight
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

#Main control loop
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

	mergedSessions, deleteRowIds = mergeSessions(sessionPairs)

	printProcessedSessions(sessionPairs, unpairedMidnightEnd, unpairedMidnightStart)
	# updateDatabase(mergedSessions)
	# deleteSessions(deleteRowIds)

if __name__ == '__main__':
	main()
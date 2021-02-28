import os
import datetime as dt
import databaseFunctions as dbf
import pandas as pd

filePath = os.path.realpath(__file__)
fileDirectory = os.path.dirname(filePath)
dirList = os.listdir(fileDirectory)

databaseName = 'legacyData.db'
databasePath = fileDirectory + '\\' + databaseName

notGames = ['Month', 'Date', 'Day', 'Total']

def findCsv():
	csvList = []
	for file in dirList:
		if file.endswith('.csv'):
			csvList.append(file)

	csvList.sort()
	return csvList

def gamesList(df):
	columns = list(df.columns)
	games = [x for x in columns if x not in notGames]

	return games

def returnYM(file):
	year, month = file.split('-')
	month, _ = month.split('.')

	return int(year), int(month)

def gameRows(game, df):
	rows = df.loc[df[game].notna(), ('Date', game)]
	rows.reset_index(inplace = True)
	rows.drop(columns = 'index', inplace = True)

	return rows

def convertDuration(duration):
	duration = dt.datetime.strptime(duration, '%Hh %Mm')
	duration = dt.timedelta(days = duration.day - 1, hours = duration.hour, minutes = duration.minute)

	return str(duration)

def main():
	dbf.createDataBase()
	csvList = findCsv()
	print(csvList)

	for file in csvList:
		print('Writing: ' + str(file))
		writeStart = dt.datetime.now()

		year, month = returnYM(file)

		df = pd.read_csv(file)
		games = gamesList(df)

		for game in games:
			rows = gameRows(game, df)
			for i in range(rows.shape[0]):
				gameRow = rows.loc[i, ['Date', game]]
				startDate = dt.datetime(year = year, month = month, day = gameRow['Date'])
				duration = convertDuration(gameRow[game])
				row = {'name': game, 'startTime': startDate, 'duration': duration}
				dbf.writeSession(row)

		writeEnd = dt.datetime.now()
		writeDuration = writeEnd - writeStart
		print(str(file) + ' written in: ' + str(writeDuration))

main()
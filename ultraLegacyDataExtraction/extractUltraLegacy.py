import os
import datetime as dt
import databaseFunctions as dbf
import pandas as pd

filePath = os.path.realpath(__file__)
fileDirectory = os.path.dirname(filePath)
dirList = os.listdir(fileDirectory)

print(fileDirectory, dirList)

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

	return year, month

def gameRows(game, df):
	rows = df.loc[df[game].notna(), ('Date', game)]
	rows.reset_index(inplace = True)
	rows.drop(columns = 'index', inplace = True)

	return rows

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
			print(rows)

		writeEnd = dt.datetime.now()
		writeDuration = writeEnd - writeStart
		print(str(file) + ' written in: ' + str(writeDuration))

main()
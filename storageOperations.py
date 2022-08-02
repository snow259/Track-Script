import sqlite3
import os

# All paths used
# filePath is path to this file, its directory is fileDirectory
filePath = os.path.realpath(__file__)
fileDirectory = os.path.dirname(filePath)
dataDirectory = fileDirectory + '\\Data'
backupDirectory = fileDirectory + '\\Backup'
databasePath = dataDirectory + '\\mainDatabase.db'
archivePath = dataDirectory + '\\archiveDatabase.db'


# Uses vacuum into to create a backup
def backupMain(mainBackupPath):
	backupMainString = 'VACUUM INTO ' + mainBackupPath
	database = sqlite3.connect(databasePath)
	try:
		database.execute(backupMainString)
	finally:
		database.close()


# Uses vacuum into to create a backup
def backupArchive(archiveBackupPath):
	backupArchiveString = 'VACUUM INTO ' + archiveBackupPath
	archive = sqlite3.connect(archivePath)
	cursor = archive.cursor()
	try:
		cursor.execute(backupArchiveString)
	finally:
		archive.close()


# Appends mainDatabase into archiveDatabase
def archive():
	attachString = 'ATTACH ? AS mainDatabase'
	attachArgument = (databasePath,)
	insertGameString = 'INSERT INTO Games(name, startTime, endTime, duration) SELECT name, startTime, endTime, duration FROM mainDatabase.Games'
	detachString = 'DETACH DATABASE mainDatabase'
	conn = sqlite3.connect(archivePath)
	cursor = conn.cursor()
	try:
		cursor.execute(attachString, attachArgument)
		cursor.execute(insertGameString)
	except Exception as e:
		print('Error in archive()')
		print(e)
		print('Rolling back!')
		conn.rollback()
	else:
		conn.commit()
	finally:
		cursor.execute(detachString)
		conn.close()


def checkForBackupDirectories():
	dirList = os.listdir(fileDirectory)
	if dirList.count('Backup') == 0:
		mainBackupDirectory = backupDirectory + '\\Main'
		archiveBackupDirectory = backupDirectory + '\\Archive'
		os.mkdir(backupDirectory)
		os.mkdir(mainBackupDirectory)
		os.mkdir(archiveBackupDirectory)


def checkForArchive():
	dirList = os.listdir(dataDirectory)
	if dirList.count('archiveDatabase.db') == 0:
		archive = sqlite3.connect(archivePath)
		cursor = archive.cursor()
		cursor.execute('CREATE TABLE Games (id INTEGER PRIMARY KEY, name TEXT NOT NULL, startTime TIMESTAMP, endTime TIMESTAMP, duration TEXT)')
		archive.close()


checkForBackupDirectories()
checkForArchive()

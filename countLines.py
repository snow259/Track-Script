import os

#Path to this file. Script counts lines in all .py files other than itself within this directory, non recursively
filePath = os.path.realpath(__file__)
fileDirectory = os.path.dirname(filePath)

listDir = os.listdir(fileDirectory)

#List of .py lines
pyList = []
for i in listDir:
	if i.endswith('.py'):
		pyList.append(i)

#Does not count itself
pyList.remove('countLines.py')
files = len(pyList)

#Counts number of lines by looking for /n
lines = 0
for file in pyList:
	with open(file) as inFile:
		fileContents = inFile.read()
	lines += fileContents.count('\n')

print('Number of files is: ' + str(files))
print('Number of lines is: ' + str(lines))

input('Press ENTER to exit')

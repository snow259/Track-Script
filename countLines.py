import os

filePath = os.path.realpath(__file__)
fileDirectory = os.path.dirname(filePath)

listDir = os.listdir(fileDirectory)

pyList = []
for i in listDir:
	if i.endswith('.py'):
		pyList.append(i)

pyList.remove('countLines.py')
files = len(pyList)

lines = 0
for file in pyList:
	with open(file) as inFile:
		fileContents = inFile.read()
	lines += fileContents.count('\n')

print('Number of files is: ' + str(files))
print('Number of lines is: ' + str(lines))

input('Press ENTER to exit')

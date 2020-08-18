from itertools import count

#Tab length 4 is used in editors, 8 appears to be used in console
tabLength = 8

def printOutput(rows):
	unpacked = unpack(rows)
	maxLengths = valueMaxLengths(unpacked)
	printStrings(unpacked, maxLengths)

def unpack(rows):
	unpacked = {'id': [], 'name': [], 'startTime': [], 'endTime': [], 'duration': []}

	for row in rows:
		for key in unpacked:
			unpacked[key].append(row[key])

	return unpacked

def valueMaxLengths(unpacked):
	maxLengths = {'id': 0, 'name': 0, 'startTime': 0, 'endTime': 0, 'duration': 0}

	#For each value under a key, check if the length is greater than value in maxLengths
	for key in unpacked:
		for value in unpacked[key]:
			if len(str(value)) > maxLengths[key]:
				length = len(str(value))
				maxLengths[key] = length

	return maxLengths

def printStrings(unpacked, maxLengths):
	#Print top row
	stringElements = {'id': '', 'name': '', 'startTime': '', 'endTime': '', 'duration': ''}
	for key in unpacked:
		stringElements[key] = key
	outString = makeString(stringElements, maxLengths)
	print(outString)

	#Print remaining rows
	iteration = count()
	iterate = True
	while iterate == True:
		i = next(iteration)
		numberOfValues = len(unpacked['id'])
		if numberOfValues == i + 1:
			iterate = False

		for key in unpacked:
			stringElements[key] = unpacked[key][i]
		outString = makeString(stringElements, maxLengths)
		print(outString)

def makeString(stringElements, maxLengths):
	tab = '	'	#Tab, not space
	outString = ''
	for key in stringElements:
		element = str(stringElements[key])
		elementLength = len(element)
		elementTabLength = -(-elementLength // tabLength)	#Upsidedown floor division becomes ceiling division
		elementTabLengthRemainder = elementLength % tabLength

		maxLength = maxLengths[key]
		maxTabLength = -(-maxLength // tabLength)
		maxTabLengthRemainder = maxLength % tabLength

		outString = outString + str(element) + tab
		
		#To determine number of additional tabs to be added after an element
		tabsRequired =  maxTabLength - elementTabLength
		tabCorrection = 0
		#If remainder == 0, the tab added after this element will form an entirely new tab space
		if elementTabLengthRemainder == 0:
			tabCorrection -= 1
		#If remainer == 0, the tab added after the element with max length will form an entirely new tab space
		#If remainder == 3, the gap between the two columns is too short, like with startTime and endTime, not needed with tab length 8 like in the console
		if maxTabLengthRemainder == 0:
			tabCorrection += 1
		#Checks if current element is the one with max length and zeroes out the additional tabs after
		if maxTabLength == elementTabLength:
			tabsRequired = 0

		outString = outString + (tabsRequired + tabCorrection) * tab

	return outString

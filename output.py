from itertools import count

# Tab length 4 is used in editors, 8 appears to be used in console
tabLength = 8


# While the following functions are key agnostic and theoretically should work on any sqlite3 row,
# some exmaples will use the most common row type found by querying the main or archive database:
# 'id', 'name', 'startTime', 'endTime', 'duration'
def printOutput(rows):
	keysList = rows[0].keys()
	# Following three functions are key agnostic, comment line within is an example of how the variable will look like when working with a complete row from Games table
	unpacked = unpack(keysList, rows)
	maxLengths = valueMaxLengths(keysList, unpacked)
	printStrings(keysList, unpacked, maxLengths)


def unpack(keysList, rows):
	# unpacked = {'id': [], 'name': [], 'startTime': [], 'endTime': [], 'duration': []}
	unpacked = {}
	for key in keysList:
		unpacked[key] = []

	for row in rows:
		for key in unpacked:
			unpacked[key].append(row[key])

	return unpacked


def valueMaxLengths(keysList, unpacked):
	# maxLengths = {'id': 2, 'name': 4, 'startTime': 9, 'endTime': 7, 'duration': 8}
	maxLengths = {}
	for key in keysList:
		maxLengths[key] = len(key)

	# For each value under a key, check if the length is greater than value in maxLengths
	for key in unpacked:
		for value in unpacked[key]:
			if len(str(value)) > maxLengths[key]:
				length = len(str(value))
				maxLengths[key] = length

	return maxLengths


def printStrings(keysList, unpacked, maxLengths):
	# Print top row
	# stringElements = {'id': '', 'name': '', 'startTime': '', 'endTime': '', 'duration': ''}
	stringElements = {}
	for key in keysList:
		stringElements[key] = ''

	for key in unpacked:
		stringElements[key] = key
	outString = makeString(stringElements, maxLengths)
	print(outString)

	# Print remaining rows
	iteration = count()
	iterate = True
	while iterate is True:
		i = next(iteration)
		numberOfValues = len(unpacked[keysList[0]])
		if numberOfValues == i + 1:
			iterate = False

		for key in unpacked:
			stringElements[key] = unpacked[key][i]
		outString = makeString(stringElements, maxLengths)
		print(outString)


def makeString(stringElements, maxLengths):
	tab = '	'		# Tab, not space
	outString = ''
	for key in stringElements:
		element = str(stringElements[key])
		elementLength = len(element)
		elementTabLength = -(-elementLength // tabLength)		# Upsidedown floor division becomes ceiling division
		elementTabLengthRemainder = elementLength % tabLength

		maxLength = maxLengths[key]
		maxTabLength = -(-maxLength // tabLength)
		maxTabLengthRemainder = maxLength % tabLength

		outString = outString + str(element) + tab

		# To determine number of additional tabs to be added after an element
		tabsRequired = maxTabLength - elementTabLength
		tabCorrection = 0
		# If remainder == 0, the tab added after this element will form an entirely new tab space
		if elementTabLengthRemainder == 0:
			tabCorrection -= 1
		# If remainer == 0, the tab added after the element with max length will form an entirely new tab space
		# If remainder == 3, the gap between the two columns is too short, like with startTime and endTime, not needed with tab length 8 like in the console
		if maxTabLengthRemainder == 0:
			tabCorrection += 1
		# Checks if current element is the one with max length and zeroes out the additional tabs after
		if maxTabLength == elementTabLength:
			tabsRequired = 0

		outString = outString + (tabsRequired + tabCorrection) * tab

	return outString

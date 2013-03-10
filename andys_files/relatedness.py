import sys
import os
import math
import collections
import numpy

def relatednessFunction(articleA, articleB, articleLinks):
	numA = 0.0
	numB = 0.0
	numAB = 0.0
	article = ''
	relatedness = 0.0

	linksA = articleLinks[articleA]
	linksB = articleLinks[articleB]
	numA = len(linksA)
	numB = len(linksB)

	for linkA in linksA:
		for linkB in linksB:
			if linkA == linkB:
				numAB += 1

	maxAB = max(numA, numB)
	minAB = min(numA, numB)

	if maxAB > 0.0 and minAB > 0.0 and numAB > 0.0:
		relatedness = (math.log(maxAB) - math.log(numAB))/(len(articleLinks) - math.log(minAB))

	return relatedness		

def getRelatednessScore(dictionary, articleLinks):
	relatednessScores = {} # dictionary of relatedness scores for each sense of a word to surrounding unambiguous words
	unambiguousWords = []
	for key, value in dictionary.iteritems():
		if len(value) == 1:
			unambiguousWords.append(key)

	for key, ambWords in dictionary.iteritems():
		if len(ambWords) > 1:
			relatedness = []
			for ambWord in ambWords:
				for unAmbWord in unambiguousWords:
					relatedness.append(relatednessFunction(ambWord, unAmbWord, articleLinks))
				relatednessResult = average(relatedness) 	
				relatednessScores[(ambWord, key)] = relatednessResult

	return relatednessScores

def average(someList):
	return numpy.mean(someList)


def getClassiferInput(commonnessTable, relatednessTable):
	result = []
	for key, value in relatednessTable.iteritems():
		sense = key[0]
		word = key[1]
		relatedness = value
		commonness = commonness[sense]

		result.append([relatedness, commonness, sense, word])

	return result

def getClassifierY(links, xList):
	output = [-1]*len(xList)
	pointer = 0
	for i in range(0, len(xList)):
		word = xList[i][3]
		sense = xList[i][2]
		pointerTemp = pointer
		while pointerTemp < len(links):
			link = links[pointerTemp]
			if word.lower() == link[1].lower():
				if sense.lower() == link[0].lower():
					if output[i] == -1:
						output[i] = 1
						break
				else:
					if output[i] == -1:
						output[i] = 0
						break
			else:
				pointerTemp += 1 
		if pointerTemp != len(links):
			pointer = pointerTemp
	
	return output


# xList = [[1, 1, 'tree(CS)', 'tree'], [1, 1, 'tree', 'tree'], [1, 1, 'dog', 'dog'], [1, 1, 'bar(law)', 'bar'], [1, 1, 'bar(drink)', 'bar'], [1, 1, 'tree(CS)', 'tree'], [1, 1, 'tree', 'tree']]
# links = [['tree', 'tree'], ['bar(drink)', 'bar'], ['tree(CS)', 'tree']]
# output = getClassifierY(links, xList)
# print output	








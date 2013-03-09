import sys
import os
import math
import collections

def relatedness(articleA, articleB, articleLinks):
	numA = 0.0
	numB = 0.0
	numAB = 0.0
	article = ''
	relatedness = 0.0
	#numOutgoing = collections.defaultdict(lambda: 0)
	#numIncoming = collections.defaultdict(lambda: 0)

	linksA = articleLinks[articleA]
	linksB = articleLinks[articleB]
	numA = len(linksA)
	numB = len(linksB)

	for linkA in linksA:
		for linkB in linksB:
			if linkA == linkB:
				numAB += 1

	# for article, links in articleLinks.iteritems():
	# 	Each link in an article counts as an instance
	# 	for link in links:
	# 		if articleA.lower() == link.lower():
	# 			numA += 1
	# 		if articleB.lower() == link.lower():
	# 			numB += 1

	# 	if articleA in links and articleB in links:
	# 		numAB += 1

	maxAB = max(numA, numB)
	minAB = min(numA, numB)

	if maxAB > 0.0 and minAB > 0.0 and numAB > 0.0:
		relatedness = (math.log(maxAB) - math.log(numAB))/(len(linksMat) - math.log(minAB))

	return relatedness		

def getRelatednessScore(dictionary):
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
					relatedness.append(relatedness(ambWord, unAmbWord))
				relatednessResult = average(relatedness) 	
				relatednessScores[(ambWord, key)] = relatednessResult

	return relatednessScores

def getClassiferInput(commonnessTable, relatednessTable):
	result = []
	for key, value in relatednessTable.iteritems():
		sense = key[0]
		word = key[1]
		relatedness = value
		commonness = commonness[sense]

		result.append([relatedness, commonness, sense, word])

	return result









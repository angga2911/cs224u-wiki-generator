import sys
import os
import math
import collections
import numpy

def relatednessFunction(articleA, articleB, articleLinks, functionNumber):
        
        # print 'calculating relatedness for ' + str(articleA) + ' and ' + str(articleB)
        articleA = articleA.lower().replace('_', ' ')
        articleB = articleB.lower().replace('_', ' ')

        numA = 0.0
        numB = 0.0
        numAB = 0.0
        article = ''
        relatedness = 0.0
        
        if not articleA in articleLinks or not articleB in articleLinks:
                return 0.0
        
        linksA = articleLinks[articleA]
        linksB = articleLinks[articleB]

        linksASet = set(linksA)
        linksBSet = set(linksB)
        numA = len(linksASet)
        numB = len(linksBSet)
        numAB = len(linksASet.intersection(linksBSet))

        maxAB = max(numA, numB)
        minAB = min(numA, numB)

        if maxAB > 0.0 and minAB > 0.0 and numAB > 0.0:
                if functionNumber == 1:
                        relatedness = (math.log(maxAB) - math.log(numAB))/(len(articleLinks) - math.log(minAB))
                elif functionNumber == 2:
                        relatedness = (math.log(numAB)+1)/(math.log(maxAB)+1)
#                 print str(maxAB)
#                 print str(minAB)
#                 print str(numAB)
#                 print str(relatedness)
#                 print '------------------'
        
        return relatedness

# articleLinks = {'Abraham_Lincoln': ['Andrew_Johnson'], 'Andrew_Johnson': ['Abraham_Lincoln']}
# articleA = 'Abraham_Lincoln'
# articleB = 'Andrew_Johnson'           

# relatedness = relatednessFunction(articleA, articleB, articleLinks)
# print relatedness

def getRelatednessScore(ambMap, articleLinks):

        articleLinks = dict((k.lower(), [v_l.lower() for v_l in v]) for k, v in articleLinks.iteritems())
        #print articleLinks

        relatednessScores = [] # dictionary of relatedness scores for each sense of a word to surrounding unambiguous words
        unambiguousWords = []
        for pair in ambMap:
                if len(pair[1]) == 1: # the list of disambiguation is 1 (which is UNambiguous)
                        unambiguousWords.append(pair[0])

        for pair in ambMap:
                if len(pair[1]) > 1:
                        for ambWord in pair[1]:
                                relatedness = []
                                for unAmbWord in unambiguousWords:
                                        relatedness.append(relatednessFunction(ambWord, unAmbWord, articleLinks,2))
                                relatednessResult = average(relatedness)        
                                relatednessScores.append([ambWord, pair[0], relatednessResult])

        return relatednessScores

def reverse_numeric(x, y):
        return y - x
#>>> sorted([5, 2, 4, 1, 3], cmp=reverse_numeric)

def findMaxN(n, someList):
        result = [-1]*n
        for i in range(0, len(someList)):
                #if someList[i] > result[-1]:
                        #result[-1] = someList[i]
                        #result = sorted(result, cmp=reverse_numeric)
                smallest = min(result)
                minIndex = result.index(min(result))
                if someList[i] > smallest:
                        result[minIndex] = someList[i]

        return result

def average(someList):
        if len(someList) > 2:
                someList = findMaxN(5, someList)
        #return numpy.mean(someList)
        return numpy.mean(someList)

# l = [3, 5, 2, 1, 6.3, 2]
# max3 = findMaxN(3, l)
# print max3

def getClassiferInput(commonnessTable, relatednessTable):
        result = []
        for key, value in relatednessTable.iteritems():
                sense = key[0]
                word = key[1]
                relatedness = value
                commonness = commonness[sense]

                result.append([relatedness, commonness, sense, word])

        return result

def getClassifierY(links, xList, wantTrivial):
    if not wantTrivial:
        output = [-1]*len(xList)
        pointer = 0
        for i in range(len(xList)):
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
    else:
        output = [-1]*len(xList)
        
        for i in range(len(links)):
            j = 0
            while j < len(xList):
                if output[j] == -1:
                    word = xList[j][3]
                    sense = xList[j][2]
                    if links[i][1].lower() == word.lower():
                        if links[i][0].lower() == sense.lower():
                            output[j] = 1
                        else:
                            output[j] = 0
                        k = j + 1
                        while k < len(xList):
                            word = xList[k][3]
                            sense = xList[k][2] 
                            if links[i][1].lower() == word.lower():
                                if links[i][0].lower() == sense.lower():
                                    output[k] = 1
                                else:
                                    output[k] = 0
                            else:
                                break
                            k = k + 1
                j += 1
            
# try to retreive the Y
        return output


# xList = [[1, 1, 'tree(CS)', 'tree'], [1, 1, 'tree', 'tree'], [1, 1, 'dog', 'dog'], [1, 1, 'bar(law)', 'bar'], [1, 1, 'bar(drink)', 'bar'], [1, 1, 'tree(CS)', 'tree'], [1, 1, 'tree', 'tree']]
# links = [['tree', 'tree'], ['bar(drink)', 'bar'], ['tree(CS)', 'tree']]
# output = getClassifierY(links, xList)
# print output  








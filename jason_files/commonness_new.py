#!/usr/bin/python

import glob, re, json, os, time
import xml.etree.cElementTree as etree
from jason_files import disambiguate as dis
from multiprocessing import Pool
from collections import Counter

namespace = "{http://www.mediawiki.org/xml/export-0.8/}"
source_dir = '500MB_FILES'

out_dir = 'COMMONNESS_MEAS'
disam_freq_map = {}

def findLinks():
    abs_dir_input = '../jason_files/500MB_FILES/500MB_*.xml'
    total_dir = glob.glob(abs_dir_input)
    totalLinks = []
    for fn in total_dir:
        #print len(total_dir)
        f = open(fn, 'r')
        xml = f.read()
        root = etree.fromstring(xml)
        links = []
        for child in root.findall('.//{0}text'.format(namespace)):
            content = child.text
            links = re.findall('\[\[(.*?)\]\]', content)
            totalLinks += links
    
    # print totalLinks
    print "Find Links Done! There are " + str(len(totalLinks)) + " links in total!"
    return Counter(totalLinks)
    
pool = Pool(processes = 100)
def findDisambiguation(start, chunkSize, dArticles):

    print "We will only get lists for disambiguation from article: " + str(start) + " to " + str(start + chunkSize)
    if start + chunkSize <= len(dArticles):
        sample = dArticles[start:(start + chunkSize)]
    else:
        sample = dArticles[start:]
    
    possibleSenses = pool.map(dis.disambiguate, sample)
    
    # possibleSensesMap = dict(zip(sample, possibleSenses))
    # print possibleSensesMap
    
    print "DONE FOR dARTICLES #: " + str(start) + " to " + str(start + chunkSize - 1)
    print "----------------"
    return possibleSenses
    
def getdArticles():
    keyPhrase = "_(disambiguation)"
    subtractOut = len(keyPhrase)
    
    dArticles = []
    f = open('title.txt', 'r')
    current = f.readline()
    while current:
        if keyPhrase in current:
            currentPhrase = current[:(-subtractOut - 1)].replace('_', ' ')
            if isAscii(currentPhrase) and isAlpha(currentPhrase):
                dArticles.append(currentPhrase) 
            # Remove the '\n' at the end of line
        current = f.readline()
    
    print "Find all disambiguation articles done! The number of disambiguation pages is: " + str(len(dArticles))
    
    # print dArticles[30000]
    # print dArticles[40000]
    return dArticles

# countMap as {'sense' : frequency}
# possibleSenses as list of lists (each inner list represents one disambiguation page links)
def calculateCommonness(countMap):
    #scoreMap = {}
    commonnessMap = {}
    dArticles = getdArticles()
    start = 0
    chunkSize = 10000
    while start < len(dArticles):
        possibleSenses = findDisambiguation(start, chunkSize, dArticles)
        for word in possibleSenses:
            totalFrequency = 0
            for sense in word:
                if sense in countMap:
                    totalFrequency += countMap[sense] 
            #scoreMap[word] = totalFrequency
            for sense in word:
                if sense in countMap:
                    if sense in commonnessMap:
                        if (countMap[sense] + 0.0) / totalFrequency > commonnessMap[sense]:
                            commonnessMap[sense] = (((countMap[sense] + 0.0) / totalFrequency) + commonnessMap[sense]) / 2.0
                    else:
                        commonnessMap[sense] = (countMap[sense] + 0.0) / totalFrequency
                # else:
    #                 # There is no clue for this word. We should treat it as a word on its own
    #                 commonnessMap[sense] = 1
        start += chunkSize
    
    print "--------"
    print "Normalized Version of Commonnness Map Has Been Calculated!!"
    print "--------"
    
    return commonnessMap
    
def isAscii(s):
    for i in range(len(s)):
        if ord(s[i]) >= 128:
            return False
    return True

def isAlpha(s, search=re.compile(r'[^a-zA-Z0-9. ]').search):
    return not bool(search(s))
    
# import time
# tic = time.clock()
if __name__ == "__main__":
    countMap = findLinks()
    commonnessMap = calculateCommonness(countMap)
    countMap = dict(countMap)
    f = open('../jason_files/commonness.txt', 'w')
    g = open('../jason_files/count.txt', 'w')
    f.write(str(commonnessMap))
    g.write(str(countMap))
# countMap = {'Adobe_Type_Manager':3, 'Alternating_Turing_machine':5, 'Andrew_Martin':2, 'Adenosine_triphosphate':20, 'Automated_theorem_proving':33, '%2B1_button':50, 'UTC%2B1':10, '%2B1_(album)':15, 'Ordinal_number_(linguistics)':55, 'Verbal_noun':20}

# print commonnessMap    
# print countMap

# toc = time.clock()
# print toc - tic

######### countMap gives the unnormalized version
######### commonnessMap gives the normalized version
######### They are dictionaries! { sense : commonness }
#########



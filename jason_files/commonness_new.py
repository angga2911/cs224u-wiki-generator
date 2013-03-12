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
    abs_dir_input = os.path.join(source_dir, '500MB_*.xml')
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
    
def findDisambiguation():

    keyPhrase = "_(disambiguation)"
    subtractOut = len(keyPhrase)
    
    dArticles = []
    f = open('title.txt', 'r')
    current = f.readline()
    while current:
        if keyPhrase in current:
            currentPhrase = current[:(-subtractOut - 1)].replace('_', ' ')
            if isAscii(currentPhrase):
                dArticles.append(currentPhrase) 
            # Remove the '\n' at the end of line
        current = f.readline()
    
    print "Find all disambiguation articles done! The number of disambiguation pages is: " + str(len(dArticles))
    
    # print dArticles[30000]
    # print dArticles[40000]
    
    start = 30000 # default is 0
    end = 80000 # default is len(dArticles)
    print "We will only get lists for disambiguation from article: " + str(start) + " to " + str(end - 1)
    sample = dArticles[start:end]

    pool = Pool(processes=100)
    possibleSenses = pool.map(dis.disambiguate, sample)
    
    # possibleSensesMap = dict(zip(sample, possibleSenses))
    # print possibleSensesMap
    
    print "Find all the senses for those articles also done! Whew!"
    
    return possibleSenses

# countMap as {'sense' : frequency}
# possibleSenses as list of lists (each inner list represents one disambiguation page links)
def calculateCommonness(possibleSenses, countMap):
    #scoreMap = {}
    commonnessMap = {}
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
    return commonnessMap
    
def isAscii(s):
    for i in range(len(s)):
        if ord(s[i]) >= 128:
            return False
    return True
    

if __name__ == '__main__':

    import time
    tic = time.clock()

    possibleSenses = findDisambiguation()
    # countMap = {'Adobe_Type_Manager':3, 'Alternating_Turing_machine':5, 'Andrew_Martin':2, 'Adenosine_triphosphate':20, 'Automated_theorem_proving':33, '%2B1_button':50, 'UTC%2B1':10, '%2B1_(album)':15, 'Ordinal_number_(linguistics)':55, 'Verbal_noun':20}
    countMap = findLinks()
    # countMap['Captain Scarlet'] = 20
    # countMap['Crafts'] = 30
    # print countMap
    commonnessMap = calculateCommonness(possibleSenses, countMap)
    print commonnessMap    
    
    toc = time.clock()
    s
    print toc - tic


from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
import collections, pickle, re, os, sys, glob
import xml.etree.cElementTree as etree
from jason_files import disambiguate as dis
from jason_files import generate_incoming_nodes as gin
from jason_files import commonness_new as cmn
from andys_files import relatedness
from pu_files import multinomialNB
from multiprocessing import Pool



def textLine(line):
        if len(line) > 0:
                if line[:2] == '[[' and line[-2:] == ']]':
                        return False
                if line[0] == '*':
                        return False
                if line[:2] == '{{' and line[-2:] == '}}':
                        return False
                return True

        return False

def removeExtraTags(line):
        line = re.sub('\[\[', '', line)
        line = re.sub('\]\]', '', line)
        #line = re.sub('<ref>..*</ref>', '', line)
        line = re.sub('{{.*?}}', '', line)
        line = re.sub('\[http.*?\]', '', line)

        return line

def ignoreUnicodes(stemmedWords):
    dummy = []
    for word in stemmedWords:
        if isAscii(word):
            dummy.append(word)
    return dummy

def isAscii(s):
    for i in range(len(s)):
        if ord(s[i]) >= 128:
            return False
    return True


def processPageLine(line, inText, infoBox, allLinks, _STOPWORDS, _ELIM, articleTitles):
        wnl = WordNetLemmatizer()
        if inText and not infoBox:
                if not '==' in line:
                        if textLine(line):
                                if '[[' in line and ']]' in line:
                                        links = re.findall('\[\[(.*?)\]\]', line)
                                        #print links
                                        for link in links:
                                                if '|' in link:
                                                        parts = re.findall("(.*?)\|(.*)", link)
                                                        partsArray = [parts[0][0], parts[0][1]]
                                                        allLinks.append(partsArray)
                                                else:
                                                        allLinks.append([link, link])
                                        if '|' in line:
                                                line = re.sub('\[\[[\w+ \(\)]+\|', '', line)
                                        line = removeExtraTags(line)
                                        for t in sent_tokenize(line):
                                                words = word_tokenize(t)
                                                stemmedWords = []
                                                for word in words:
                                                        if not word.lower() in _STOPWORDS:
                                                                word = wnl.lemmatize(word)
                                                        if not word.lower() in _ELIM:
                                                                stemmedWords.append(word)

                                                #for i in xrange(0, len(stemmedWords)):
                                                stemmedWords = ignoreUnicodes(stemmedWords)
                                                
                                                index = 0
                                                numWords = len(stemmedWords)
                                                while index < numWords:
                                                        currWord = stemmedWords[index]
                                                        currWord = currWord[0].upper()+currWord[1:]
                                                        if index < numWords - 1:
                                                                nextWord = stemmedWords[index+1]
                                                                nextWord = nextWord[0].upper()+nextWord[1:]
                                                                
                                                                if index < numWords - 2:
                                                                        next2Word = stemmedWords[index+2]
                                                                        next2Word = next2Word[0].upper()+next2Word[1:]
                                                                        trigram = currWord + '_' + nextWord + '_' + next2Word
                                                                        #trigram = trigram.replace('.', '')

                                                                        """
                                                                        Check to see if trigram/bigram/unigram is in the list-
                                                                        """

                                                                        if articleTitles[trigram] == 1:
                                                                                ## print 'here'
                                                                                ## print trigram
                                                                                termsNeeded.append(trigram)
                                                                                #trigramAmbWords = disambiguate.disambiguate(trigram)
                                                                                #ambMap.append([trigram, trigramAmbWords])
                                                                                index += 3
                                                                        else:
                                                                                bigram = currWord + '_' + nextWord
                                                                                if articleTitles[bigram] == 1:
                                                                                    ## print bigram
                                                                                    termsNeeded.append(bigram)
                                                                                    #bigramAmbWords = disambiguate.disambiguate(bigram)
                                                                                    #ambMap.append([bigram, bigramAmbWords])
                                                                                    ## print bigram
                                                                                    index += 2
                                                                                else:
                                                                                        if len(currWord) > 3 and (not currWord.lower() in _STOPWORDS):
                                                                                            unigram = currWord
                                                                                            if articleTitles[unigram] == 1:
                                                                                                ## print unigram
                                                                                                termsNeeded.append(unigram)
                                                                                                #unigramAmbWords = disambiguate.disambiguate(unigram)
                                                                                                #ambMap.append([unigram, unigramAmbWords])
                                                                                                ## print unigramAmbWords
                                                                                        index += 1
                                                                else:
                                                                        bigram = currWord + '_' + nextWord
                                                                        if articleTitles[bigram] == 1:
                                                                            #print bigram
                                                                            termsNeeded.append(bigram)
                                                                            #bigramAmbWords = disambiguate.disambiguate(bigram)
                                                                            #ambMap.append([bigram, bigramAmbWords])
                                                                            index += 2
                                                                        else:
                                                                            index += 1
                                                        else:
                                                                if len(currWord) > 3 and (not currWord.lower() in _STOPWORDS):
                                                                        unigram = currWord
                                                                        if articleTitles[unigram] == 1:
                                                                      #     #print unigram
                                                                            termsNeeded.append(unigram)
                                                                            #unigramAmbWords = disambiguate.disambiguate(unigram)
                                                                            #ambMap.append([unigram, unigramAmbWords])
                                                                index += 1

def preProcessLine(line):
        line = line.strip()
        line = re.sub('&lt;', '<', line)
        line = re.sub('&gt;', '>', line)
        line = re.sub('&quot;', '"', line)
        line = re.sub('&apos;', "'", line)
        line = re.sub('&amp;', '&', line)

        return line

def buildAmbMap(listOfLines, articleTitles):

#    if not os.path.isfile(file_path):
    _STOPWORDS = ['the', 'a', 'an', 'of', 'in', 'on', 'about', 'what', 'which', 'when', 'why', 'how', 'is', 'was', 
    'are', 'were', 'am', 'i', 'as', 'to', 'and', "'s", ',', '.', '(', ')', 'with', '/', 'but', 'not', 'dids']

    _ELIM = ['the']

    # pkl_file = open('articleTitles.pkl', 'rb')
    # articleTitles = pickle.load(pkl_file)
    # pkl_file.close()
    
    # inPage = False
    inPage = True
    inText = False
    infoBox = True
    lastLine = ''
    allLinks = []

    for line in listOfLines:
            line = preProcessLine(line)
    
            if '<text' in line:
                    inText = True
            if '</text>' in line:
                    inText = False
    
            if '{{Infobox' in line or '{{Persondata' in line:
                    infoBox = True;
            if infoBox and lastLine == '}}':
                    infoBox = False;
    
            if inPage:
                    processPageLine(line, inText, infoBox, allLinks, _STOPWORDS, _ELIM, articleTitles)
    
            lastLine = line
       
#     No longer need to store ambiguity map
#     file_path = 'AMBIGUITY_MAP/ambiguity.py' 
#     
#     ambi = open(file_path,'a')
#     for row in ambMap:
#         ambi.write(str(row))
#     
#     ambi.close()


def buildRelatedness(ambMap):
    relatednessPath = '../andys_files/relatedness.txt'
    print "Calculating relatedness..."

    scores = relatedness.getRelatednessScore(ambMap, articleLinks)
    
    print "-- Relatedness score table for this article --"
    for score in scores:
        print score
    print "----------------------------------------------"
    
    return scores

def combine_rc(R, C, readFromFileR, readFromFileC, normalized):
    
    print "We are in the RC combining process."
    
    if readFromFileR:
        
        rpath = '../andys_files/relatedness.txt'
        print 'Currently reading R from file ' + rpath
        
        if not os.path.isfile(rpath):
                print "The R file you are looking for does not exist"
                return
        rfile = open(rpath, 'r')
        save = rfile.read()
        temp = 'R =' + save
        exec temp
        
        print "Finish reading R from file!"
    
    if readFromFileC:   
        if normalized:
            cpath = '../jason_files/commonness.txt'
        else:
            cpath = '../jason_files/count.txt'
            
        print 'Currently reading C from file ' + cpath
    
        if not os.path.isfile(cpath):
                print "The C file you are looking for does not exist"
                return
        cfile = open(cpath, 'r')
        save = cfile.read()
        temp = 'C =' + save
        exec temp
        
        print "Finish reading C from file!"
        
        #### Data Structure
        ####
        # R is a list in this structure [[s,w,r],[s2,w2,r2],...]
        # C is a dictionary {s:c, s2:c2, ...}
        
        #print R
        #raw_input()

    print "Combining R and C into X matrix ..."
    for sense in R:
       dummySense = sense[0].replace('_',' ')
       if dummySense in C:
           sense.append(C[dummySense]) # get the corresponding commonnness for that sense
       else:
           # print "There's no such sense"
           sense.append(1.0)

    return R
    
def findLinks(wikiFile):
    abs_dir_input = wikiFile
    total_dir = glob.glob(abs_dir_input)
    totalLinks = []
    for fn in total_dir:
        #print len(total_dir)
        f = open(fn, 'r')
        links = re.findall('\[\[(.*?)\]\]', f.read())
        links = [[link.replace(' ','_').split('|')[0], link.replace(' ','_').split('|')[-1]] for link in links if isAlpha(link)] 
        totalLinks += links
    return totalLinks

def isAlpha(s, search=re.compile(r'[^a-zA-Z0-9. _(),|]').search):
    #Note period, space, parenthese, and underscore are allowed.
    return not bool(search(s))
    
### GLOBALS ###

namespace = "{http://www.mediawiki.org/xml/export-0.8/}"
termsNeeded = []
articleLinks = gin.income()
pool = Pool(processes = 120)

###############

if __name__ == '__main__':


    if len(sys.argv) != 5:
        sys.exit("Need 4 arguments: usefileforR? usefileforC? normalizedC? wikiFile")

    readFromFileR = 0 if sys.argv[1] == '0' else 1
    readFromFileC = 0 if sys.argv[2] == '0' else 1
    normalized = 0 if sys.argv[3] == '0' else 1
    
    wikiFile = sys.argv[4]
    
    
    # just dummy initialization to pass into function
    R = []
    C = []
    
    if not readFromFileR:
        # We should build for each article one by one
        # We first extract pages from wikiFile
        
        print "We are NOT going to read R from file"
            
#         No longer need to show ambiguity map   
#         out_dir = 'AMBIGUITY_MAP'
#         if not os.path.exists(out_dir):
#             os.makedirs(out_dir)     
#         file_path = 'AMBIGUITY_MAP/ambiguity.py'
#         ambi = open(file_path,'w')
#         ambi.write('[')
#         ambi.close()
        
        print "Trying to retrieve all titles ... (take long!) "
        
        articleTitles = collections.defaultdict(lambda: 0)
        f = open('title.txt', 'r')
        for line in f:
        #print line.strip()
            articleTitles[line.strip()] = 1
        f.close()
        
        print "Finish retrieving titles"
        
        pages = open(wikiFile, 'r')
        tempText = []
        inPage = 0
        
        print "Will process each wiki page by page (starting from page 1)"
        pageNumber = 0
        
        ambMapList = []
        
        n = 0
        
        
        for line in pages:
            
            line = preProcessLine(line)
            if '</page>' in line:
                tempText.append(line)
                inPage = 0
                # The page is complete. We can build ambiguity map from here
                
                print "Collecting n-grams and building disambiguation list from page# " + str(pageNumber)
                
                buildAmbMap(tempText, articleTitles)
                
                print "Building disambiguation map"
                
                disambList = pool.map(dis.disambiguate, termsNeeded)
                ambMap = [[termsNeeded[i], disambList[i]] for i in range(len(termsNeeded))]
                #print ambMap
                ambMapList.append(ambMap)
                
                termsNeeded = []
                # This will update the termsNeeded
                tempText = []
                
                n += 1
                
                # do this every 10 page to prevent memory overload
                if n % 10 == 0:
                    RList = pool.map(buildRelatedness, ambMapList)
                    for r in RList:
                        R += r
                    ambMapList = []

            elif inPage == 1:
                tempText.append(line)
            elif '<page>' in line:
                pageNumber += 1
                print "We are in page " + str(pageNumber)
                tempText.append(line)
                inPage = 1


        #for r in R:
        #    print r
        
#         No longer need to show ambiguity map
#         file_path = 'AMBIGUITY_MAP/ambiguity.py'
#         ambi = open(file_path,'a')      
#         ambi.write(']')
#         ambi.close()
        
        relatednessPath = '../andys_files/relatedness.txt'
        relatednessFile = open(relatednessPath, 'w')
        relatednessFile.write(str(R))
        relatednessFile.close()
        
    else:
        print "We are going to read R from file"   
#         file_path = 'AMBIGUITY_MAP/ambiguity.py'    
#         f = open(file_path, 'r')
#         save = f.read()
#         exec 'ambMap =' + save 
        
    if not readFromFileC:
        print "We are NOT going to reading C from file"
        C = cmn.findLinks() # This is the count dictionary
        if normalized:
            C = cmn.calculateCommonness(C) # This is the "commonness" dictionary (i.e. normalized count)
    else:
        print "We are going to reading C from file"
    
    # user_input = raw_input()
    X = combine_rc(R, C, readFromFileR, readFromFileC, normalized)
    # X = combine_rc(R, C2, False, False)
    X = [[x[2], x[3], x[0], x[1]] for x in X] # Reorder to get [r c s w]
    # for x in X:
    #     print x
    
    totalLinks = findLinks(wikiFile)
    Y = relatedness.getClassifierY(totalLinks, X, True)
    for i in range(min(len(X), len(totalLinks))):
        print str(X[i]) + '\t\t\t' + str(totalLinks[i])
    print Y
    
    newX = []
    newY = []
    for i in range(len(Y)):
        if Y[i] != -1:
            newX.append(X[i])
            newY.append(Y[i])
    X = newX
    Y = newY 
    
    results = multinomialNB.runAll(X, Y, X, Y) # The last two needs to be changed to the real one NOT THE PREDICTED ONE
    
    for result in results:
        print result
    
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
import collections, pickle, re, os, sys, glob
import xml.etree.cElementTree as etree
from jason_files import disambiguate
from jason_files import generate_incoming_nodes as gin
from jason_files import commonness_new as cmn
from andys_files import relatedness
from pu_files import multinomialNB

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


def processPageLine(line, inText, infoBox, allLinks, ambMap, _STOPWORDS, _ELIM, articleTitles):
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
                                                                                trigramAmbWords = disambiguate.disambiguate(trigram)
                                                                                ambMap.append([trigram, trigramAmbWords])
                                                                                index += 3
                                                                        else:
                                                                                bigram = currWord + '_' + nextWord
                                                                                if articleTitles[bigram] == 1:
                                                                                    ## print bigram
                                                                                    bigramAmbWords = disambiguate.disambiguate(bigram)
                                                                                    ambMap.append([bigram, bigramAmbWords])
                                                                                    ## print bigram
                                                                                    index += 2
                                                                                else:
                                                                                        if len(currWord) > 3 and (not currWord.lower() in _STOPWORDS):
                                                                                                unigram = currWord
#                                                                                               if articleTitles[unigram] == 1:
#                                                                                                       ## print unigram
#                                                                                                       unigramAmbWords = disambiguate.disambiguate(unigram)
#                                                                                                       ambMap.append([unigram, unigramAmbWords])
#                                                                                                       ## print unigramAmbWords
                                                                                        index += 1
                                                                else:
                                                                        bigram = currWord + '_' + nextWord
                                                                        if articleTitles[bigram] == 1:
                                                                                #print bigram
                                                                                bigramAmbWords = disambiguate.disambiguate(bigram)
                                                                                ambMap.append([bigram, bigramAmbWords])
                                                                                index += 2
                                                                        else:
                                                                                index += 1
                                                        else:
                                                                if len(currWord) > 3 and (not currWord.lower() in _STOPWORDS):
                                                                        unigram = currWord
                                                                        # if articleTitles[unigram] == 1:
#                                                                       #       #print unigram
#                                                                               unigramAmbWords = disambiguate.disambiguate(unigram)
#                                                                               ambMap.append([unigram, unigramAmbWords])
                                                                index += 1

                                #print line

def preProcessLine(line):
        line = line.strip()
        line = re.sub('&lt;', '<', line)
        line = re.sub('&gt;', '>', line)
        line = re.sub('&quot;', '"', line)
        line = re.sub('&apos;', "'", line)
        line = re.sub('&amp;', '&', line)

        return line

def buildAmbMap(wikiFile):
    file_path = 'AMBIGUITY_MAP/ambiguity.py'
#    if not os.path.isfile(file_path):
    _STOPWORDS = ['the', 'a', 'an', 'of', 'in', 'on', 'about', 'what', 'which', 'when', 'why', 'how', 'is', 'was', 
    'are', 'were', 'am', 'i', 'as', 'to', 'and', "'s", ',', '.', '(', ')', 'with', '/', 'but', 'not', 'dids']

    _ELIM = ['the']

    articleTitles = collections.defaultdict(lambda: 0)
    f = open('title.txt', 'r')
    for line in f:
    #print line.strip()
            articleTitles[line.strip()] = 1
    f.close()

    # pkl_file = open('articleTitles.pkl', 'rb')
    # articleTitles = pickle.load(pkl_file)
    # pkl_file.close()

    f = open(wikiFile, 'r')
    
    inPage = False
    inText = False
    infoBox = True
    lastLine = ''
    allLinks = []
    ambMap = []
    for line in f:
            line = preProcessLine(line)
    
            if line == '<page>':
                    inPage = True
            if line == '</page>':
                    inPage = False
    
            if '<text' in line:
                    inText = True
            if '</text>' in line:
                    inText = False
    
            if '{{Infobox' in line or '{{Persondata' in line:
                    infoBox = True;
            if infoBox and lastLine == '}}':
                    infoBox = False;
    
            if inPage:
                    processPageLine(line, inText, infoBox, allLinks, ambMap, _STOPWORDS, _ELIM, articleTitles)
    
            lastLine = line
    
    f.close()

    out_dir = 'AMBIGUITY_MAP'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
        
    ambi = open(file_path,'w')
    ambi.write(str(ambMap))

    return ambMap

def buildRelatedness(ambMap, articleLinks):
    relatednessPath = '../andys_files/relatedness.txt'
    print "Calculating relatedness..."
    relatednessFile = open(relatednessPath, 'w')
    scores = relatedness.getRelatednessScore(ambMap, articleLinks)
    for score in scores:
        print score
    relatednessFile.write(str(scores))    
    return scores

def combine_rc(R, C, readFromFileR, readFromFileC, normalized):
    
    if readFromFileR:
        rpath = '../andys_files/relatedness.txt'
        if not os.path.isfile(rpath):
                print "no r file"
                return
        rfile = open(rpath, 'r')
        save = rfile.read()
        temp = 'R =' + save
        exec temp
    
    if readFromFileC:   
        if normalized:
            cpath = '../jason_files/commonness.txt'
        else:
            cpath = '../jason_files/count.txt'
        if not os.path.isfile(cpath):
                print "no c file"
                return
        cfile = open(cpath, 'r')
        save = cfile.read()
        temp = 'C =' + save
        exec temp
        
        #### Data Structure
        ####
        # R is a list in this structure [[s,w,r],[s2,w2,r2],...]
        # C is a dictionary {s:c, s2:c2, ...}
        
        #print R
        #raw_input()
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

###############

if __name__ == '__main__':

    if len(sys.argv) != 5:
        sys.exit("Need 4 arguments: usefileforR? usefileforC? normalizedC? wikiFile")

    readFromFileR = 0 if sys.argv[1] == '0' else 1
    readFromFileC = 0 if sys.argv[2] == '0' else 1
    normalized = 0 if sys.argv[3] == '0' else 1
    
    wikiFile = sys.argv[4]
    
    articleLinks = gin.income()
    
    # just dummy initialization to pass into function
    R = 0
    C = 0
    print readFromFileR, readFromFileC, normalized
    if not readFromFileR:
        ambMap = buildAmbMap(wikiFile)
        R = buildRelatedness(ambMap, articleLinks) # This is the relatedness matrix
    else:
        file_path = 'AMBIGUITY_MAP/ambiguity.py'    
        f = open(file_path, 'r')
        save = f.read()
        exec 'ambMap =' + save 
        
    if not readFromFileC:
        C = cmn.findLinks() # This is the count dictionary
        if normalized:
            C = cmn.calculateCommonness(C) # This is the "commonness" dictionary (i.e. normalized count)
    
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
    
    results = multinomialNB.runBoth(X, Y, X, Y) # The last two needs to be changed to the real one NOT THE PREDICTED ONE
    
    for result in results:
        print result
    
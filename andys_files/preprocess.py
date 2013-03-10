import re
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
import collections
import pickle

_STOPWORDS = ['the', 'a', 'an', 'of', 'in', 'on', 'about', 'what', 'which', 'when', 'why', 'how', 'is', 'was', 
	'are', 'were', 'am', 'i', 'as', 'to', 'and', "'s", ',', '.', '(', ')', 'with', '/', 'but', 'not', 'dids']

_ELIM = ['the']

articlesTitles = collections.defaultdict(lambda: 0)
f = open('title.txt', 'r')
for line in f:
	#print line.strip()
	articlesTitles[line.strip()] = 1
f.close()

# pkl_file = open('articlesTitles.pkl', 'rb')
# articlesTitles = pickle.load(pkl_file)
# pkl_file.close()

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

def processPageLine(line, inText, infoBox, allLinks):
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
									if articlesTitles[trigram] == 1:
										#print 'here'
										print trigram
										# trigramAmbWords = disambiguate(trigram)
										# ambMap[trigram] = trigramAmbWords
										index += 3
									else:
										bigram = currWord + '_' + nextWord
										if articlesTitles[bigram] == 1:
											# bigramAmbWords = disambiguate(bigram)
											# ambMap[bigram] = bigramAmbWords
											print bigram
											index += 2
										else:
											if len(currWord) > 3 and (not currWord.lower() in _STOPWORDS):
												unigram = currWord
												if articlesTitles[unigram] == 1:
													print unigram
													# unigramAmbWords = disambiguate(unigram)
													# ambMap[unigram] = unigramAmbWords
											index += 1
								else:
									bigram = currWord + '_' + nextWord
									if articlesTitles[bigram] == 1:
										print bigram
										# bigramAmbWords = disambiguate(bigram)
										# ambMap[bigram] = bigramAmbWords
										index += 2
									else:
										index += 1
							else:
								if len(currWord) > 3 and (not currWord.lower() in _STOPWORDS):
									unigram = currWord
									if articlesTitles[unigram] == 1:
									 	print unigram
										# unigramAmbWords = disambiguate(unigram)
										# ambMap[unigram] = unigramAmbWords
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

f = open('tiny-wiki.xml', 'r')

inPage = False
inText = False
infoBox = True
lastLine = ''
allLinks = []
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
		processPageLine(line, inText, infoBox, allLinks)

	lastLine = line

f.close()
#print allLinks


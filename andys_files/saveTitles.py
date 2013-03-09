import pickle
import collections

#articlesTitles = collections.defaultdict(lambda: 0)
articlesTitles = {}
f = open('title.txt', 'r')
for line in f:
	#print line.strip()
	articlesTitles[line.strip()] = 1
output = open('articlesTitles.pkl', 'wb')
pickle.dump(articlesTitles, output)
f.close()
output.close()


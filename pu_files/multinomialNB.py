import numpy as np
from dataForNB import *

X = [[elem[0], elem[1]] for elem in raw] # relatedness and commonness
senseTag = [elem[2] for elem in raw] # which sense it comes from
indicator = [elem[3] for elem in raw] # which word it comes from
 
X = np.array(X)
Y = np.array(rawY)

from sklearn.naive_bayes import MultinomialNB
clf = MultinomialNB()
clf.fit(X, Y)
MultinomialNB(alpha = 0.1, class_prior = None, fit_prior = True)
q = clf.predict_proba(X)
print q
r = clf.predict(X)
print r

all = []
maxprob = []

setOfIndicator = set(indicator)
for i in setOfIndicator:
  temp = []
  for j in range(len(raw)):
    if raw[j][3] == i:
      temp.append([i, senseTag[j], q[j][1]])
  all.append(sorted(temp, key = lambda temp: temp[2], reverse = True))

for item in all:
    print "Word #: " + str(item[0][0]) + " Label number: " + str(item[0][1]) +  " with probability: " + str(item[0][2])


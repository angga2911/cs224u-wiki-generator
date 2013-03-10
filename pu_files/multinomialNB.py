import numpy as np
from dataForNB import *
import SVM as support
import evaluation as evaluation
from sklearn.naive_bayes import MultinomialNB, BernoulliNB

def multinomialNB(): 
  X = np.array([[elem[0], elem[1]] for elem in raw]) # relatedness and commonness
  senses = [elem[2] for elem in raw] # which sense it comes from
  words = [elem[3] for elem in raw] # which word it comes from
 
  Y = np.array(rawY)


  clf = BernoulliNB(alpha = 0.0, class_prior = None, fit_prior = True)
  # clf = MultinomialNB(alpha = 0.1, class_prior = None, fit_prior = True)
  clf.fit(X, Y)
  
  
  # This part needs to be changed to a sample

  sampleX = np.array([[elem[0], elem[1]] for elem in rawXTesting])
  sampleY = np.array(rawYTesting)
  
  q = clf.predict_proba(sampleX)
  predictedProb = [elem[1] for elem in q]


  predictedY = evaluation.getPredictedY(words, senses, predictedProb)
  print evaluation.evaluationMetrics(sampleY, predictedY)
  
# return precision, recall, f1 of binary lists

def main(): 
  print "\n\nMultinomial NB\n\n"
  multinomialNB()
  print "\n\nSVM\n\n"
  support.supportFunction()

if __name__ == '__main__':
  main()

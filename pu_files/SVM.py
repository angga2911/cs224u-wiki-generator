from sklearn import svm
from dataForNB import *
import evaluation as evaluation

def supportFunction():
  X = [elem[0:1] for elem in raw]
  Y = rawY
  senses = [elem[2] for elem in raw]
  words = [elem[3] for elem in raw]
  #modelr = svm.SVR()
  modelr = svm.SVC(kernel = 'poly', degree = 2, probability = True)
  modelr.fit(X,Y)
  
  # This part needs to be changed to sample
    
  sampleX = [elem[0:1] for elem in rawXTesting]
  sampleY = rawYTesting
  q = modelr.predict_proba(sampleX)
  predictedProb = [elem[1] for elem in q]
  
  predictedY = evaluation.getPredictedY(words, senses, predictedProb)
  print evaluation.evaluationMetrics(sampleY, predictedY)
  

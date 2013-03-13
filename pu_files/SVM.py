from sklearn import svm as sup
import evaluation as evaluation

def supportFunction(rawX, rawY, rawXTesting, rawYTesting):
  X = [elem[0:1] for elem in rawX]
  Y = rawY
  senses = [elem[2] for elem in rawX]
  words = [elem[3] for elem in rawX]
  #modelr = svm.SVR()
  modelr = sup.SVC(kernel = 'poly', degree = 2, probability = True)
  modelr.fit(X,Y)
  
  # This part needs to be changed to sample
    
  sampleX = [elem[0:1] for elem in rawXTesting]
  sampleY = rawYTesting
  q = modelr.predict_proba(sampleX)
  predictedProb = [elem[1] for elem in q]
  
  predictedY = evaluation.getPredictedY(words, senses, predictedProb, rawXTesting, rawYTesting)
  return evaluation.evaluationMetrics(sampleY, predictedY)
  

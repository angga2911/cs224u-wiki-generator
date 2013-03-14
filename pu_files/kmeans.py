from sklearn import cluster
import evaluation as evaluation

def kmeansFunction(rawX, rawY, rawXTesting, rawYTesting):
  X = [elem[0:1] for elem in rawX]
  Y = rawY
  senses = [elem[2] for elem in rawX]
  words = [elem[3] for elem in rawX]
  
  
  modelk = cluster.KMeans(n_clusters = 2)  
  modelk.fit(X)
  
  # This part needs to be changed to sample
    
  sampleX = [elem[0:1] for elem in rawXTesting]
  sampleY = rawYTesting
  q = modelk.transform(sampleX)
  # This gives distance to the new "clusters"
  predictedProb = [-elem[1] for elem in q]
  # Note we use negative since we want lower distance!
  
  predictedY = evaluation.getPredictedY(words, senses, predictedProb, rawXTesting, rawYTesting)
  return evaluation.evaluationMetrics(sampleY, predictedY)
  

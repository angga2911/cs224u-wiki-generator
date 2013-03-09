from sklearn import svm
X = [[0.1, 0.99], [0.5, 0.80], [0.70, 0.1], [0.01, 0.01], [0.2, 0.95], [0.25, 0.01], [0.5, 0.02], [0.5, 0.999], [0.4, 0.95], [0.3, 0.91]]

Y = [1, 0, 0, 0, 1, 0, 0, 1, 1, 1]

modelr = svm.SVR()
modelr.fit(X,Y)
print modelr.predict(X)
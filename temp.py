import numpy as np
import pandas as pd
from LogisticRegression import LogisticRegression
import featureSelection as fs
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.model_selection import KFold, LeaveOneOut, train_test_split
from sklearn.metrics import mean_squared_error as mse
import sys
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression as LR


master = pd.read_csv('alldata.csv')

y = master['peak_count']
X = master.drop('peak_count', 1)

y = np.array(y)

mu = np.mean(y)
sigma = np.std(y)
count, bins, ignored = plt.hist(y, 10, normed=True)
plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (bins - mu)**2 / (2 * sigma**2) ), linewidth=2, color='r')
plt.title('Peak Count distribution')
plt.show()

###
sys.exit()
###

X = X.drop('t',1)

plt.hist(y)
plt.show()

y = np.round(np.array(y))

y[y < 3] = 0
y[y > 2] = 1
print(y)


X = np.array(X)

featureMask = fs.forClassification(X, y, 3)
print(featureMask)



seta = SelectKBest(f_classif, k=5)
seta.fit(X, y)
print(seta.get_support())
featureMask = seta.get_support()
logreg = LogisticRegression()
#logreg = LR()

X_train, X_test, y_train, y_test = train_test_split(X[:,featureMask], y, test_size=0.33, random_state=42)

logreg.fit(X_train,y_train)

def dummy(array):
    return np.ones(array.shape[0], dtype=np.int8)

prediction = logreg.predict(X_test)
testError = mse(y_test, prediction)
dummyError = mse(y_test, dummy(X_test))
print('Test error: ' + str(testError))
print('Dummy error: ' + str(dummyError))

print(prediction)
print(y_test)
print(np.sum(y_test == prediction))
#print(np.sum(y_test != prediction))

#plt.show()

#print(np.sum(dummy(X_test) == y_test))


sys.exit()

kf = KFold(n_splits=10)
error = 0
for traincv, validationcv in kf.split(X):
    X_train, X_val = X[traincv,:], X[validationcv,:]
    y_training, y_validation = y[traincv], y[validationcv]

    theta = logreg.fit(X_train, y_training)

    error += mse(y_validation, logreg.predict(X_val))

print('Error was: ' + str(error/10))
print(logreg.prob)
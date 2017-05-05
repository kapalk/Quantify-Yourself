import numpy as np
import pandas as pd
from scipy.optimize import minimize, fmin_bfgs
from sklearn.datasets import load_iris


class LogisticRegression():
    """Logistic regression machine learning algorithm"""
    def __init__(self):
        self.fitted = False
        self.predicted = False
        self.theta = None
        self.prob = None

    def fit(self, X, y):
        """Minimizes the cost function and creates prediction model for data"""
        theta = np.zeros((X.shape[1] + 1, 1))
        features = np.ones((X.shape[0], X.shape[1] + 1))
        features[:, 1:] = X
        labels = np.squeeze(y)
        self.theta = fmin_bfgs(self.cost, theta, fprime=self.gradient, args=(features, labels))
        self.fitted = True
        print('Prediction Model Created.')
        return self.theta

    def predict(self, X):
        """Performs prediction on data"""
        if self.fitted:
            data = np.ones((X.shape[0], X.shape[1] + 1))
            data[:, 1:] = X
            self.prob = self.sigmoid(self.theta, data)
            pred = np.where(self.prob >= 0.5, 1, 0)
            self.prediction = pred
            self.predicted = True
            return self.prediction
        else:
            print('Model has not been fitted. Cannot predict. Aborting.')

    def sigmoid(self, theta, X):
        """Sigmoid function for Logistic Regression"""
        return 1.0 / (1.0 + np.exp(-X.dot(theta)))

    def cost(self, theta, X, y):
        """Cost function for Logistic Regression"""
        p = self.sigmoid(theta, X)
        return ((-y) * np.log(p) - (1 - y) * np.log(1 - p)).mean()

    def gradient(self, theta, X, y):
        """Derivative of cost function"""
        error = self.sigmoid(theta, X) - y
        return error.T.dot(X) / y.size

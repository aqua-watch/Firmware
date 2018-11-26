# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 14:00:44 2018

@author: Armin
"""

import time

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import scipy as sp
import scipy.sparse.linalg as linalg
import scipy.cluster.hierarchy as hr
from scipy.spatial.distance import pdist, squareform

import sklearn.datasets as datasets
import sklearn.metrics as metrics
import sklearn.utils as utils
import sklearn.linear_model as linear_model
import sklearn.svm as svm
import sklearn.model_selection as cross_validation # Code for cross validation.
import sklearn.cluster as cluster
from sklearn.ensemble import AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import StandardScaler

import statsmodels.api as sm

from patsy import dmatrices

import seaborn as sns

from importlib import reload
from datetime import datetime
from IPython.display import Image
from IPython.display import display_html
from IPython.display import display
from IPython.display import Math
from IPython.display import Latex
from IPython.display import HTML


from getTestingSet import createTestingSet
import formatModels

from matplotlib.colors import ListedColormap


model_df = formatModels.formatModel()
#split data
X = []
y = []
for idx, row in model_df.iterrows():
        X.append([row["Cond"], row["PH"],row["ORP"],row["TDS"], row["Turb"]])
        y.append(row["Contaminated"])
(X_train, X_test, y_train, y_test) = cross_validation.train_test_split(
        X, y, test_size=0.4)

svc = svm.SVC(kernel='linear')
svc.fit(X_train, y_train)
y_pred_test = svc.predict(X_test)
print("Accuracy of SVM test set:", svc.score(X_test, y_test))


# Create color maps for 3-class classification problem, as with iris
cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF'])
cmap_bold = ListedColormap(['#FF0000', '#00FF00', '#0000FF'])

def plot_estimator(estimator, X, y):
    try:
        (X, y) = (X.values, y.values)
    except AttributeError:
        pass
    
    #estimator.fit(X, y)
    (x_min, x_max) = min(X[:][0]) - .1, max(X[:][ 0]) + .1
    (y_min, y_max) = min(X[:][ 1]) - .1, max(X[:][ 1]) + .1
    print("gang with my gang")
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 100),
                         np.linspace(y_min, y_max, 100))
    
    #Z = estimator.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = estimator.predict(X_test)
    print("gang")
    # Put the result into a color plot.
    #Z = Z.reshape(xx.shape)
    plt.figure()
    plt.pcolormesh(xx, yy, Z, cmap=cmap_light)

    # Plot also the training points.
    plt.scatter(X[:][0], X[:][ 1], c=y, cmap=cmap_bold)
    plt.axis('tight')
    plt.axis('off')
    plt.tight_layout()
    
    
plot_estimator(svc, X, y)


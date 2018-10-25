# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 14:34:21 2018

@author: Armin
"""
import json
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.datasets.samples_generator import make_blobs
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import formatModels

def build_model(model_df):
    #split data
    X = []
    y = []
    for idx, row in model_df.iterrows():
        X.append([row["Cond"], row["PH"],row["ORP"],row["TDS"], row["Turb"]])
        y.append(row["Contaminated"])
        
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42, stratify= y)
    #clf = LogisticRegression(random_state = 0, solver='lbfgs',
    #                      multi_class='multinomial').fit(X_train, y_train)
    clf = LogisticRegression().fit(X_train, y_train)
    
    print("Accuracy on training dataset: ({0:.6f}) ".format( clf.score(X_train , y_train)))
    print("Accuracy on testing dataset: ({0:.6f}) ".format( clf.score(X_test , y_test)))

    x = [[
			0.7851929043577127,
			-0.694250653265955,
			 0.20470726985476198,
			 1.8716911902092956,
			 -0.5969549024403896
		]]
    
    result = clf.predict(x)
    #print(len(result))
    print(result)
    
    
model_df = formatModels.formatModel()
build_model(model_df)

#print(model_df)


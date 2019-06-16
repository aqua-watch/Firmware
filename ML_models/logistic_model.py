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
import sys



sys.path.insert(0, '../')
from getTestingSet import createTestingSet

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
    
    """
    testingModel = createTestingSet()
    
    total = len(testingModel)
    correct = 0
    incorrect = 0
    
    for exp in testingModel:
        #print([list(exp["value"].values())[0:5]])
        res = clf.predict([list(exp["value"].values())[0:5]]) #0-5 only because we did not train on temp
        if(res == 1 and exp["contaminated"] == 1 or res == 0 and exp["contaminated"] == 0):
            correct += 1
        else:
            incorrect += 1
            
    
            
    print("Accuracy on mixed testing set: ({0:.6f}) ".format(correct / total))
    
    """
    
    #result = clf.predict(x)
    #print(len(result))
    #print(result)
    
    
contaminated_model_df = formatModels.formatModel(["../Models/phase_1/model_absolute.json"])
uncontaminated_model_df = formatModels.formatModel(["../Models/ChemDptSamples/unContWater_absolute.json",
                                                    "../Models/ChemDptSamples/deion_absolute.json",
                                                    "../Models/ChemDptSamples/Filterred_water_absolute.json"])
    
contaminted_ppb_samples = formatModels.formatModel(["../Models/ChemDptSamples/0.03pb_absolute.json",
                                                    "../Models/ChemDptSamples/0.3pb_absolute.json",
                                                    "../Models/ChemDptSamples/3pb_absolute.json"
                                                    ,"../Models/ChemDptSamples/30pb_absolute.json",
                                                    "../Models/ChemDptSamples/300pb_absolute.json",
                                                    "../Models/ChemDptSamples/20pb_absolute.json",
                                                    "../Models/ChemDptSamples/10pb_absolute.json"])
#build_model(

print("===============================================")    
    
#print(contaminated_model_df.append(uncontaminated_model_df))

build_model(contaminated_model_df.append(uncontaminated_model_df).append(contaminted_ppb_samples))
print("===============================================")    

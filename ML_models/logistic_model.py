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
        #X.append([row["Cond"], row["PH"],row["ORP"],row["TDS"], row["Turb"]])
        X.append([row["Cond"], row["PH"],row["ORP"]])
        y.append(row["Contaminated"])
        
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42, stratify= y)
    #clf = LogisticRegression(random_state = 0, solver='lbfgs',
    #                      multi_class='multinomial').fit(X_train, y_train)
    
    clf = LogisticRegression().fit(X_train, y_train)
    
    print("Accuracy on training dataset: ({0:.6f}) ".format( clf.score(X_train , y_train)))
    print("Accuracy on testing dataset: ({0:.6f}) ".format( clf.score(X_test , y_test)))
    
    return clf
    

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

print("===============================================")    
    

clf = build_model(contaminated_model_df.append(uncontaminated_model_df).append(contaminted_ppb_samples))
print("===============================================")    

print("Testing againts FeNi samples: ")

fe_ni_samples = formatModels.formatModel(["../Models/iron_samples/3000pb_absolute.json",
                                                    "../Models/iron_samples/300pb_absolute.json",
                                                    "../Models/iron_samples/80ppm_absolute.json",
                                                    "../Models/iron_samples/30pb_absolute.json",
                                                    "../Models/iron_samples/stock_solution_absolute.json"])
    
fe_ni_samples.drop(['Desc', 'Timestamp', 'Contaminated', 'TDS', 'Turb'], inplace=True, axis=1)
total_predictions = 0
temp = clf.predict(fe_ni_samples)
pos = 0

for i in temp:
    pos += i
    
print("Total positives: %d"%pos)
print("Total negatives %d"% (int(len(temp))-pos))
    
    

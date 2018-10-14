# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 14:34:21 2018

@author: Armin
"""
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.datasets.samples_generator import make_blobs
import pandas as pd
import numpy as np


def formatModel():
    #take our json object and convert to tabular format
    model = {}  
    with open('model_0.json') as f:
        model = f.read().replace('\n', '')
        model = json.loads(model)
    model_df = pd.DataFrame([], columns = ['Cond','PH', 'ORP', 'TDS', 'Turb', 'Desc', 'Timestamp'])  
    experiments =  model["Exps"]
    ix = 0 #index of df
    for exp in experiments:
        insert = []
        desc = exp["desc"]
        ts = exp["timeStamp"]
        
        for result in exp["results"]:
            insert = []
            insert.append(result["Conductivity"])
            insert.append(result["PH"])
            insert.append(result["ORP"])
            insert.append(result["Turp"])
            insert.append(result["TDS"])
            insert.append(desc)
            insert.append(ts)
            
            model_df.loc[ix] = (insert)
            ix += 1
            
    
    return model_df

def test_model(model_df):
    
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

model_df = formatModel()
print(model_df)


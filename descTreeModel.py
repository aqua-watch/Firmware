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
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
import graphviz
from sklearn.tree import export_graphviz
from sklearn.tree import _tree
import os
os.environ["PATH"] += os.pathsep + 'D:/Program Files (x86)/Graphviz2.38/bin/'
def build_model(model_df):
    #split data
    X = []
    y = []
    for idx, row in model_df.iterrows():
        X.append([row["Cond"], row["PH"],row["ORP"],row["TDS"], row["Turb"]])
        y.append(row["Contaminated"])
        
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42, stratify = y)
    tree = DecisionTreeClassifier(max_depth=4, random_state=0, max_leaf_nodes=10 )
    tree.fit(X_train, y_train)
    
    print("Accuracy on training dataset: ({0:.6f}) ".format( tree.score(X_train , y_train)))
    print("Accuracy on testing dataset: ({0:.6f}) ".format( tree.score(X_test , y_test)))

    x = [[ #expecting uncontaminated
			0.7851929043577127,
			-0.694250653265955,
			 0.20470726985476198,
			 1.8716911902092956,
			 -0.5969549024403896
		]]
    
    result = tree.predict(x)
    #print(len(result))
    print(result)
    tree_to_code(tree, ['Cond','PH', 'ORP', 'TDS', 'Turb'])
    
    #and print
    dot_data = export_graphviz(tree, out_file='descTreeExample.dot', class_names=['Contaminated', 'Uncontaminated'], feature_names=['Cond','PH', 'ORP', 'TDS', 'Turb'],
               impurity=False, filled=True)
    dot_data = export_graphviz(tree, out_file=None, 
                         feature_names=['Cond','PH', 'ORP', 'TDS', 'Turb'],  
                        
                         filled=True, rounded=True,  
                         special_characters=True) 
    graph = graphviz.Source(dot_data) 
    graph.render("descTreeExample") 
    
def tree_to_code(tree, feature_names):
    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]
    print("def tree({}):".format(", ".join(feature_names)))

    def recurse(node, depth):
        indent = "  " * depth
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]
            print("{}if {} <= {}:".format(indent, name, threshold))
            recurse(tree_.children_left[node], depth + 1)
            print("{}else:  # if {} > {}".format(indent, name, threshold))
            recurse(tree_.children_right[node], depth + 1)
        else:
            print("{}return {}".format(indent, tree_.value[node]))

    recurse(0, 1)
model_df = formatModels.formatModel()
build_model(model_df)

#print(model_df)


# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 10:28:29 2018

@author: Armin
"""
import json
from pprint import pprint
import numpy as np
import math
import datetime
import sys


def queryPoint(query, model = None):
    if(model == None):
        model = {}
        with open('model.json') as f:
            model = f.read().replace('\n', '')
            model = json.loads(model)
        #left todo
            

def centerPoint(data_set):
    avgs = []
    for i in range(0, len(data_set) - 1):
        r_avg = 0.0
        for j in range(0, len(data_set) - 1):
            if(i == j): continue
            r_avg += euclideanDistance(data_set[i], data_set[j])
        
        avgs.append(r_avg / len(data_set))
    
    min_val = (0, 1.7976931348623157e+308)
    
    for idx in range(0, len(avgs)-1):
        if(avgs[idx] < min_val[1]):
            min_val = (idx, avgs[idx])
            
            
    print(min_val)
    return data_set[min_val[0]]

def euclideanDistance(instance1, instance2):
	distance = 0
	for k, v in instance1.items():
		distance += pow((instance1[k] - instance2[k]), 2)
	return math.sqrt(distance)

def addToModel(add):
    #load the model first
    model = {}
    with open('model.json') as f:
        model = f.read().replace('\n', '')
        model = json.loads(model)
        
    with open('model.json', 'w') as f:
            model['Exps'].append(add)
            pprint(model)
            json.dump(model, f)

def openLatestOutput():
    with open('log_putty_output.json') as f:
        data = f.read().replace('\n', '').split("~=\"Con")[1]
        return json.loads(data) 
        
def normalizeDataSet(dataSet):
    for data in dataSet:
        mean = sum(data.values()) / len(data.values())
        std = np.std(list(data.values()))
        for k,v in data.items():
            data[k] = (v - mean) / std
        
    return dataSet

   
def main():
    print("Your actions are 0 for loading latest data set from output file and adding to model \n or 1 for querying a data point from the output file")
    action = int(input())
    if(action == 0):
        data = openLatestOutput()
        normalized_data = normalizeDataSet(data[list(data.keys())[0]])
        center = centerPoint(normalized_data)
        final_obj = {}
        final_obj[list(data.keys())[0]] = {
                    "desc" : 'some stuff',
                    "results" : data[list(data.keys())[0]],
                    "center" : center
                }
        addToModel(final_obj)
        pprint("Done!")
    elif(action == 1):
        pprint("Done!")

main()
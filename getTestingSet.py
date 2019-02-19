# -*- coding: utf-8 -*-
"""
Created on Sun Nov  4 20:14:29 2018

@author: Armin
"""
import json


def createTestingSet():
    testing_set = []
    model = {}
    with open('../Models/distilled_water_model_absolute.json') as f:
        model = f.read().replace('\n', '')
        model = json.loads(model)   
        
    un_cont_counter = 0
    cont_counter = 0
        
    for exp in model["Exps"]:
        if(exp["contaminated"] == 0 and un_cont_counter < 3):
            un_cont_counter += 1
            i = 0
            for i in range(0, 30):
                testing_set.append({'contaminated':0, 'value':exp["results"][i]})
        elif(exp["contaminated"] == 1 and cont_counter < 3):
            cont_counter += 1
            i = 0
            for i in range(0, 30):
                testing_set.append({'contaminated':1, 'value':exp["results"][i]})
                
    model = {}
    with open('../Models/tap_water_absolute.json') as f:
        model = f.read().replace('\n', '')
        model = json.loads(model) 
    for exp in model["Exps"]:
        if(exp["contaminated"] == 0 ):
            
            i = 0
            for i in range(0, 30):
                testing_set.append({'contaminated':0, 'value':exp["results"][i]})
        elif(exp["contaminated"] == 1 and cont_counter < 3):
            cont_counter += 1
            i = 0
            for i in range(0, 30):
                testing_set.append({'contaminated':1, 'value':exp["results"][i]})    
    
    model = {}
    with open('../Models/ChemDptSamples/0.03pb_absolute.json') as f:
        model = f.read().replace('\n', '')
        model = json.loads(model) 
    
    for exp in model["Exps"]:
        if(exp["contaminated"] == 0 ):
            print(len(exp["results"]))
            i = 0
            for i in range(0, 30):
                testing_set.append({'contaminated':0, 'value':exp["results"][i]})
        elif(exp["contaminated"] == 1 ):
            cont_counter += 1
            i = 0
            for i in range(0, 30):
                testing_set.append({'contaminated':1, 'value':exp["results"][i]})    
        
    #print(len(testing_set))
    return testing_set

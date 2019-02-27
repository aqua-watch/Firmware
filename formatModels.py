# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 16:16:24 2018

@author: Armin
"""
import json
import pandas as pd
import os, sys

MODEL_DIR = "../Models/"
NORM_MODEL_PATH = MODEL_DIR + "distilled_water_model_norm.json"
ABS_MODEL_PATH =  MODEL_DIR + "distilled_water_model_absolute.json"

def formatModel(models =  [
                        "../Models/ChemDptSamples/30pb_absolute.json",
                        "../Models/ChemDptSamples/300pb_absolute.json",
                        "../Models/ChemDptSamples/3000pb_absolute.json",
                        "../Models/ChemDptSamples/10pb_absolute.json",
                        "../Models/ChemDptSamples/20pb_absolute.json",
                        "../Models/ChemDptSamples/deion_absolute.json"]):
    #take our json object and convert to tabular format
    model_df = pd.DataFrame([], columns = ['Cond','PH', 'ORP', 'TDS', 'Turb', 'Desc', 'Timestamp', 'Contaminated',])  
    ix = 0 #index of df
    total_num_contaminated = 0
    for model_name in models:
        
        model = {}  
        with open(model_name) as f:
            model = f.read().replace('\n', '')
            model = json.loads(model)
        experiments =  model["Exps"]
        
        for exp in experiments:
            print(model_name + " Experiment sample size: " + str(len(exp["results"])))
            insert = []
            desc = exp["desc"]
            ts = exp["timeStamp"]
            contaminated = exp["contaminated"]
            total_num_contaminated += contaminated
            for result in exp["results"]:
                insert = []
                insert.append(result["Conductivity"])
                insert.append(result["PH"])
                insert.append(result["ORP"])
                insert.append(result["Turp"])
                insert.append(result["TDS"])
                insert.append(desc)
                insert.append(ts)
                insert.append(contaminated)
                model_df.loc[ix] = (insert)
                ix += 1
    
    print("================================================")
    print("Precentange of contaminated models:")
    print(total_num_contaminated/len(models))
    return model_df

def formatModel_extra_dims():
    #take our json object and convert to tabular format
    model = {}  
    with open('Models/test_arm_absolute.json') as f:
        model = f.read().replace('\n', '')
        model = json.loads(model)
        
    model_norm = {}  
    with open('Models/test_arm_norm.json') as f:
        model_norm = f.read().replace('\n', '')
        model_norm = json.loads(model_norm)
        
        
    model_df = pd.DataFrame([], columns = ['Cond','PH', 'ORP', 'TDS', 'Turb', 'Cond_norm', 'PH_norm', 'ORP_norm',
                            'TDS_norm', 'Turb_norm'
                            , 'Desc', 'Timestamp', 'Contaminated'])  
    experiments =  model["Exps"]
    experiments_norm =  model_norm["Exps"]
    
    ix = 0 #index of df
    exp_idx = 0

    
    
    for exp in experiments:
        res_idx = 0
        insert = []
        desc = exp["desc"]
        ts = exp["timeStamp"]
        contaminated = exp["contaminated"]
        
        for result in exp["results"]:
            insert = []
            insert.append(result["Conductivity"])
            insert.append(result["PH"])
            insert.append(result["ORP"])
            insert.append(result["Turp"])
            insert.append(result["TDS"])
            insert.append(experiments_norm[exp_idx]["results"][res_idx]["Conductivity"])
            insert.append(experiments_norm[exp_idx]["results"][res_idx]["PH"])
            insert.append(experiments_norm[exp_idx]["results"][res_idx]["ORP"])
            insert.append(experiments_norm[exp_idx]["results"][res_idx]["Turp"])
            insert.append(experiments_norm[exp_idx]["results"][res_idx]["TDS"])
            insert.append(desc)
            insert.append(ts)
            insert.append(contaminated)
            
            model_df.loc[ix] = (insert)
            ix += 1
            res_idx += 1
            
        exp_idx += 1
            
    
    return model_df

def get_normalized_values_json():
    #take our json object and convert to tabular format
    model = {}  
    with open(NORM_MODEL_PATH) as f:
        model = f.read().replace('\n', '')
        model = json.loads(model)
        
    return model

def get_normalized_values_from_json(model):
    model_df = pd.DataFrame([], columns = ['Cond','PH', 'ORP', 'TDS', 'Turb', 'Desc', 'Timestamp', 'Contaminated'])  
    experiments =  model["Exps"]
    ix = 0 #index of df
    for exp in experiments:
        insert = []
        desc = exp["desc"]
        ts = exp["timeStamp"]
        contaminated = exp["contaminated"]
        
        for result in exp["results"]:
            insert = []
            insert.append(result["Conductivity"])
            insert.append(result["PH"])
            insert.append(result["ORP"])
            insert.append(result["Turp"])
            insert.append(result["TDS"])
            insert.append(desc)
            insert.append(ts)
            insert.append(contaminated)
            
            model_df.loc[ix] = (insert)
            ix += 1
            
    
    return model_df

def get_absolute_values_json():
    #take our json object and convert to tabular format
    model = {}  
    with open(ABS_MODEL_PATH) as f:
        model = f.read().replace('\n', '')
        model = json.loads(model)
        
    return model

def get_absolute_values_from_json(model):
    model_df = pd.DataFrame([], columns = ['Cond','PH', 'ORP', 'TDS', 'Turb', 'Desc', 'Timestamp', 'Contaminated'])  
    experiments =  model["Exps"]
    ix = 0 #index of df
    for exp in experiments:
        insert = []
        desc = exp["desc"]
        ts = exp["timeStamp"]
        contaminated = exp["contaminated"]
        
        for result in exp["results"]:
            insert = []
            insert.append(result["Conductivity"])
            insert.append(result["PH"])
            insert.append(result["ORP"])
            insert.append(result["Turp"])
            insert.append(result["TDS"])
            insert.append(desc)
            insert.append(ts)
            insert.append(contaminated)
            
            model_df.loc[ix] = (insert)
            ix += 1
            
    
    return model_df


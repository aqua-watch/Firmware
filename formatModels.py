# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 16:16:24 2018

@author: Armin
"""
import json
import pandas as pd
import os, sys
from pprint import pprint


MODEL_DIR = "../Models/"

NORMAL_COLS = ['Cond','PH', 'ORP', 'TDS', 'Turb', 'Desc', 'Timestamp', 'Contaminated',]
EXTENDED_COLS = ['Cond','PH', 'ORP', 'TDS', 'Turb', 'Cond_norm', 'PH_norm', 'ORP_norm', 'TDS_norm', 'Turb_norm', 'Desc', 'Timestamp', 'Contaminated']

def formatModel(models = [
                            MODEL_DIR + "ChemDptSamples/30pb_absolute.json",
                            MODEL_DIR + "ChemDptSamples/300pb_absolute.json",
                            MODEL_DIR + "ChemDptSamples/3000pb_absolute.json",
                            MODEL_DIR + "ChemDptSamples/10pb_absolute.json",
                            MODEL_DIR + "ChemDptSamples/20pb_absolute.json",
                            MODEL_DIR + "ChemDptSamples/deion_absolute.json"]):
    #take our json object and convert to tabular format
    model_df = pd.DataFrame([], columns=NORMAL_COLS)  
    ix = 0 #index of df
    total_num_contaminated = 0
    center_points = {}
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
            center_points[desc] = exp["center_point"]
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
    print("================================================")
    print("Center Points:")
    print(center_points)
    
    
    return model_df

def formatModel_extra_dims():
    #take our json object and convert to tabular format
    model = get_model_json(MODEL_DIR + 'test_arm_absolute.json')
    model_norm = get_model_json(MODEL_DIR + 'test_arm_norm.json')
        
    model_df = pd.DataFrame([], columns=EXTENDED_COLS)  
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

def get_model_json(model_path):
    #take our json object and convert to tabular format
    model = {}  
    with open(model_path) as f:
        model = f.read().replace('\n', '')
        model = json.loads(model)
        
    return model

def get_values_from_json(model_json):
    model_df = pd.DataFrame([], columns=NORMAL_COLS)  
    experiments =  model_json["Exps"]
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


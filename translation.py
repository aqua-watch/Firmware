# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 20:01:32 2019

@author: asabouri
"""
import json
import collections
import math

def euclideanDistance(instance1, instance2):
	distance = 0
	for k, v in instance1.items():
		distance += pow((instance1[k] - instance2[k]), 2)
	return math.sqrt(distance)

def queryPoint(query, model_name = None):
    if(model_name == None):
        model = {}
        with open('model.json') as f:
            model = f.read().replace('\n', '')
            model = json.loads(model)
        #left todo
    else: 
        model = {}
        with open(model_name) as f:
            model = f.read().replace('\n', '')
            model = json.loads(model)
    
    dists = {}
    for exp in model["Exps"]:    
        dist = euclideanDistance(query, exp["center_point"])
        dists[dist] = exp
        
    #sort our dict of distances and clusters according to the smallest distance
    od = collections.OrderedDict(sorted(dists.items()))
    closest_n = od[list(od.keys())[0]]
    closest_n_standard_deviation_0 = closest_n["standard_deviation"]
    closest_n["results"].append(query)
    
    closest_n_standard_deviation_1 = standard_dev_cluster(closest_n["results"], closest_n["center_point"])
    
    
    diff_stand_dev = {}
    for k,v in closest_n_standard_deviation_0.items():
        diff_stand_dev[k] = closest_n_standard_deviation_1[k] - v
        
    rsum = 0.0
    idx = 0
    for _, v in diff_stand_dev.items():
        idx += 1
        rsum += v
    print(rsum, float(idx))
    if rsum >= .7:
        return 0 #false
    else:
        return 1 #true
    
def standard_dev_cluster(data_set, center_point, dims = 5):
    mean_center = sum(list(center_point.values())) / dims
    keys = list(data_set[1])
    standard_devs = {}
    for i in range(0, dims):
        t1 = [list(data_set[j].values())[i] for j in range(0, len(data_set))]
        mean_t1 = list(center_point.values())[i]
        rsum = 0.0
        for el in t1:
            rsum += math.pow(el - mean_t1, 2)
            
        standard_devs[keys[i]] = math.sqrt(rsum / (dims - 1))
    return standard_devs

def centerPoint(data_set, dims = 6):
    center = [0] * dims
    for i in range(0, dims): #for the i'th dimension
        try:
           sample = [list(data_set[j].values())[i] for j in range(0, len(data_set)) ]
        except IndexError:
           print('not enough keys')
        rsum = 0.0
        members = 2 * len(sample)
        for el in sample: #for each data point in the ith dimension
            # 2 * (xi - el) => (2 * len(sample)) + rsum (2 * el) = 0
            rsum += 2 * el
            
        center[i] = (rsum) / members
        #center[i] = (-1 * rsum) / members
    
    center_dict = {}
    idx = 0
    for key in list(data_set[0]):
        center_dict[key] = center[idx]
        idx += 1
    return center_dict

def getLabledModel(models):
    model = []
    for m in models:
        with open(m) as f:
            temp = f.read().replace('\n', '')
            model.append(json.loads(temp))
            
    return model
        
def getContaminatedModel(model_name, time_increments=15):
    TIME_INCREMENT = time_increments #min per sample
    
    time_count = 0
    model = {}
    with open(model_name) as f:
        model = f.read().replace('\n', '')
        model = json.loads(model)
    for exp in model['Exps']: #for each set of experimentation we increase the time increment
        if(not exp["contaminated"] == 0):
            exp["time_after_contamination"] = time_count
            time_count += TIME_INCREMENT
    
    return model

def getAverageCenterPoint(exp_object):
    """
    @param: experiment object
    @return: average center point of experiment object
    """
    average = {}
    count = 0
    for exp in exp_object["Exps"]:
        for metric, center_point in exp["center_point"].items():
            try:
                average[metric] += center_point
            except :
                average[metric] = center_point
        count += 1        
    
    for k,v in average.items():
        average[k] = v / count
    
    return average

def getModelsppbFromDesc(model):
    #this should be replaced with another field in the exp object -- > amount_of_contamination
    return model["Exps"][0]["ppb_amount_contamination"]

def getPpb(queryCenterPoint, labledModels):
    RANGE = 50
    distances = []
    
    in_range_labled_model = []
    
    for model in labledModels:
        distance = euclideanDistance(queryCenterPoint, model["avg_center_points"])
        distances.append(distance)
       
        model['distance_to_query'] = distance
        if distance < RANGE:
            continue
    
        in_range_labled_model.append(model)
        
        
    #compute a labled clusters weight
    distance_sum = sum(distances)
    ppb = 0
    
    for model in in_range_labled_model:
        weight = (distance_sum - model["distance_to_query"]) / distance_sum
        models_contamination_amount = getModelsppbFromDesc(model)
        ppb += weight * models_contamination_amount
 
    print(str(ppb) + " Ppb ====== " + labledModels)
    return ppb
        

def getMapping():
    
    labledSamples = [
                        "./Models/ChemDptSamples/3000pb_absolute.json",
                        "./Models/ChemDptSamples/300pb_absolute.json",
                        "./Models/ChemDptSamples/30pb_absolute.json",
                        "./Models/ChemDptSamples/10pb_absolute.json",
                        "./Models/ChemDptSamples/20pb_absolute.json"]
    timedModel = getContaminatedModel('./Models/distilled_water_model_norm.json', 15)
    labledModels = getLabledModel(labledSamples)
    #add an average center point to each experimetn in the labled model
    for model in labledModels:
        model['avg_center_points'] = getAverageCenterPoint(model)
    
    #test each exp in timed experiment set
    for exp in timedModel["Exps"]:
        getPpb(exp["center_point"], labledModels)

    
    
getMapping()
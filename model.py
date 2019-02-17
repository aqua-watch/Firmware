# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 10:28:29 2018

@author: Armin
"""
import json
from pprint import pprint
import numpy as np
import math
import collections
import datetime
import serial

from getTestingSet import createTestingSet
import sys
sys.path.insert(0, '../')
import formatModels


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
        
def closestPoint(data_set):
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
            
   
    return data_set[min_val[0]]

def euclideanDistance(instance1, instance2):
	distance = 0
	for k, v in instance1.items():
		distance += pow((instance1[k] - instance2[k]), 2)
	return math.sqrt(distance)

def addToModel(add, fileName = None):
    if fileName == None: 
        fileName = 'model.json'
    
    #load the model first
    model = {}
    with open(fileName) as f:
        model = f.read().replace('\n', '')
        model = json.loads(model)
        
    with open(fileName, 'w+') as f:
            model['Exps'].append(add)
            pprint(model)
            json.dump(model, f)

def testAccuracy():
    testingModel = createTestingSet()
    total = len(testingModel)
    correct = 0
    incorrect = 0
    model = 'Models/distilled_water_model_absolute.json'
    for exp in testingModel:
        query_point = exp["value"]
        print( exp["contaminated"])
        res = queryPoint(query_point, model )
        if(res == 1 and exp["contaminated"] == 1 or res == 0 and exp["contaminated"] == 0):
            correct += 1
        else:
            incorrect += 1
            
    print("Accuracy on mixed testing set: ({0:.6f}) ".format(correct / total))

def openLatestOutput():
    with open('log_putty_output.txt') as f:
        try:
            data = f.read().replace('\n', '').split("~=\"Con")[1]
        except:
            data = ''
                
        return json.loads(data) 
        
def readFromSerialPort():
    ser = serial.Serial(
            port='\\.\COM4',\
            baudrate=9600
    )

    print("connected to: " + ser.portstr)
    data = str(ser.readline(), 'utf-8').replace('\r\n','')
        
    ser.close()
    return json.loads(data) 
    
def normalizeDataSet(dataSet):
    cp_data  = dataSet
    
    for data in cp_data:
        mean = sum(data.values()) / len(data.values())
        std = np.std(list(data.values()))
        for k,v in data.items():
            data[k] = (v - mean) / std
        
    return cp_data

def normalizeMinMax(dataset):
    """
    @param: Array of objects 
    
    """
    cp_data  = dataSet
    inverted = {}
    
    #for each metric compute its min and max
    for sample in dataset:
        for metric, v in sample.items():
            if(type(inverted[metric]) == 'list'):
                inverted[metric].append(v)
            else:
                inverted[metric] = [v]
                
    for sample in cp_data:
        for metric, v in sample.items():
            sample[metric] = (v - min(inverted[metric])) / max(inverted[metric]) - min(inverted[metric])
    return cp_data

def main():
    print("Your actions are 0 for loading latest data set from output file and adding to model \n or 1 for querying a data point from the output file")
    action = int(input())
    if(action == 0):
        data = openLatestOutput()
        #data = readFromSerialPort()
        absolute = data[list(data.keys())[0]]
        center_point_absolute = centerPoint(absolute)
        closest_point_absolute = closestPoint(absolute)
        standards_absolute = standard_dev_cluster(absolute, center_point_absolute)
        ##for our absolute samples
        
        final_obj = {
                    "timeStamp": datetime.datetime.today().strftime('%Y-%m-%d'),
                    "desc" : 'W/ 20 ppb lead',
                    "contaminated" : 1,
                    "ppb_amount_contamination":10,
                    "results" : data[list(data.keys())[0]], #array of objects [{ph:,cond:,...},...]
                    "closest_point" : closest_point_absolute,
                    "center_point"  : center_point_absolute,
                    'standard_deviation': standards_absolute
                }
        addToModel(final_obj, "Models/ChemDptSamples/20pb_absolute.json")
        normalized_data = normalizeMinMax(data[list(data.keys())[0]])
        print(data[list(data.keys())[0]])
        
        center_point = centerPoint(normalized_data)
        closest_point = closestPoint(normalized_data)
        standards = standard_dev_cluster(normalized_data, center_point)
        
       
        final_obj = {
                    "timeStamp": datetime.datetime.today().strftime('%Y-%m-%d'),
                    "desc" : 'W/ 20 ppb lead',
                    "contaminated" : 1,
                    "ppb_amount_contamination":10,
                    "results" : data[list(data.keys())[0]],
                    "closest_point" : closest_point,
                    "center_point"  : center_point,
                    'standard_deviation': standards
                }
        addToModel(final_obj, "Models/ChemDptSamples/20pb_norm.json")
        
        pprint("Done!")
    elif(action == 1):
        query = {'Conductivity': -0.8729087463837244, 'PH': -0.8448048541963021, 'ORP': 1.8116158462914003, 'TDS': -0.3918962550174805, 'Turp': 0.2979940093061065}
        print(queryPoint(query))
        testAccuracy()
        
        pprint("Done!")

def insert_model(modelName, dataset = None):
    
        if(dataset == None):
            data = openLatestOutput()
        else:
            #string so conver to dict object 
            data = json.loads(dataset) 
            
        absolute = data[list(data.keys())[0]]
        center_point_absolute = centerPoint(absolute)
        closest_point_absolute = closestPoint(absolute)
        standards_absolute = standard_dev_cluster(absolute, center_point_absolute)
        ##for our absolute samples
        final_obj = {}
        final_obj = {
                    "timeStamp": str(datetime.datetime.now()),
                    "desc" : 'Tap Water',
                    "contaminated" : 0,
                    "results" : data[list(data.keys())[0]],
                    "closest_point" : closest_point_absolute,
                    "center_point"  : center_point_absolute,
                    'standard_deviation': standards_absolute
                }
        addToModel(final_obj, "Models/" + modelName + "_absolute.json")
        normalized_data = normalizeDataSet(data[list(data.keys())[0]])
        
        
        center_point = centerPoint(normalized_data)
        closest_point = closestPoint(normalized_data)
        standards = standard_dev_cluster(normalized_data, center_point)
     
        final_obj = {}
        final_obj = {
                    "timeStamp": str(datetime.datetime.now()),
                    "desc" : 'Tap Water',
                    "contaminated" :0,
                    "results" : data[list(data.keys())[0]],
                    "closest_point" : closest_point,
                    "center_point"  : center_point,
                    'standard_deviation': standards
                }
        addToModel(final_obj, "Models/" + modelName + "_norm.json")
        
        pprint("Done!")

main()
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


def queryPoint(query, model = None):
    if(model == None):
        model = {}
        with open('model.json') as f:
            model = f.read().replace('\n', '')
            model = json.loads(model)
        #left todo
    
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
    if rsum >= .45:
        return 0 
    else:
        return 1
    

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

def centerPoint(data_set, dims = 5):
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
    #load the model first
    model = {}
    with open('model.json') as f:
        model = f.read().replace('\n', '')
        model = json.loads(model)

    
    queries_no_lead = model["Exps"][0]["results"][10:40]
    queries_w_lead = model["Exps"][2]["results"][10:40]
   
    correct_no_lead = correct_w_lead = 0
    for query in queries_no_lead:
        res = queryPoint(query)
        if(res == 0): #expecting false
            correct_no_lead += 1
    for query in queries_w_lead:
        res = queryPoint(query)
        if(res == 1): #expecting true
            correct_w_lead += 1
    
    print("Amount of correct w lead: " , correct_w_lead)
    print("Amount of correct no lead: " , correct_no_lead)
    accuracy_w_cont = correct_w_lead / len(queries_w_lead)
    accuracy_no_cont = correct_no_lead / len(queries_no_lead)
    print("Accuracy with contaminant: " + str(accuracy_w_cont) + "\n With out contaminant: " + str(accuracy_no_cont))

def openLatestOutput():
    with open('log_putty_output.txt') as f:
        try:
            data = f.read().replace('\n', '').split("~=\"Con")[1]
        except:
            data = '{" 9/20/2018 ":[{"Conductivity":1.57, "PH":9.30, "ORP":291.00, "TDS":162.46, "Turp": 232.04},{"Conductivity":1.54, "PH":9.25, "ORP":305.00, "TDS":166.22, "Turp": 232.04},{"Conductivity":1.54, "PH":9.30, "ORP":276.00, "TDS":162.46, "Turp": 232.04},{"Conductivity":1.54, "PH":9.26, "ORP":198.00, "TDS":162.46, "Turp": 249.23},{"Conductivity":1.54, "PH":9.23, "ORP":271.00, "TDS":162.46, "Turp": 232.04},{"Conductivity":1.57, "PH":9.28, "ORP":217.00, "TDS":162.46, "Turp": 232.04},{"Conductivity":1.57, "PH":9.16, "ORP":149.00, "TDS":166.22, "Turp": 232.04},{"Conductivity":1.54, "PH":9.14, "ORP":208.00, "TDS":166.22, "Turp": 232.04},{"Conductivity":1.57, "PH":9.19, "ORP":149.00, "TDS":162.46, "Turp": 232.04},{"Conductivity":1.54, "PH":9.14, "ORP":134.00, "TDS":166.22, "Turp": 232.04},{"Conductivity":1.57, "PH":9.21, "ORP":291.00, "TDS":166.22, "Turp": 232.04},{"Conductivity":1.57, "PH":9.25, "ORP":227.00, "TDS":166.22, "Turp": 232.04},{"Conductivity":1.54, "PH":9.25, "ORP":295.00, "TDS":162.46, "Turp": 232.04},{"Conductivity":1.57, "PH":9.30, "ORP":286.00, "TDS":162.46, "Turp": 232.04},{"Conductivity":1.54, "PH":9.25, "ORP":222.00, "TDS":162.46, "Turp": 232.04},{"Conductivity":1.54, "PH":9.25, "ORP":251.00, "TDS":162.46, "Turp": 232.04},{"Conductivity":1.54, "PH":9.26, "ORP":164.00, "TDS":162.46, "Turp": 232.04},{"Conductivity":1.54, "PH":9.16, "ORP":139.00, "TDS":162.46, "Turp": 232.04},{"Conductivity":1.54, "PH":9.16, "ORP":208.00, "TDS":166.22, "Turp": 232.04},{"Conductivity":1.57, "PH":9.18, "ORP":149.00, "TDS":162.46, "Turp": 232.04},{"Conductivity":1.54, "PH":9.14, "ORP":134.00, "TDS":162.46, "Turp": 232.04},{"Conductivity":1.54, "PH":9.19, "ORP":193.00, "TDS":166.22, "Turp": 249.23},{"Conductivity":1.54, "PH":9.19, "ORP":95.00, "TDS":162.46, "Turp": 232.04},{"Conductivity":1.54, "PH":9.16, "ORP":183.00, "TDS":162.46, "Turp": 232.04},{"Conductivity":1.54, "PH":9.30, "ORP":281.00, "TDS":162.46, "Turp": 232.04},{"Conductivity":1.54, "PH":9.25, "ORP":232.00, "TDS":162.46, "Turp": 232.04},{"Conductivity":1.57, "PH":9.25, "ORP":291.00, "TDS":162.46, "Turp": 232.04},{"Conductivity":1.54, "PH":9.30, "ORP":271.00, "TDS":166.22, "Turp": 232.04},{"Conductivity":1.54, "PH":9.23, "ORP":271.00, "TDS":166.22, "Turp": 232.04},{"Conductivity":1.57, "PH":9.23, "ORP":208.00, "TDS":166.22, "Turp": 232.04},{"Conductivity":1.54, "PH":9.18, "ORP":139.00, "TDS":166.22, "Turp": 232.04},{"Conductivity":1.57, "PH":9.14, "ORP":139.00, "TDS":166.22, "Turp": 232.04},{"Conductivity":1.54, "PH":9.19, "ORP":183.00, "TDS":166.22, "Turp": 232.04},{"Conductivity":1.57, "PH":9.14, "ORP":208.00, "TDS":166.22, "Turp": 232.04},{"Conductivity":1.57, "PH":9.23, "ORP":291.00, "TDS":166.22, "Turp": 232.04},{"Conductivity":1.57, "PH":9.30, "ORP":217.00, "TDS":166.22, "Turp": 232.04},{"Conductivity":1.54, "PH":9.25, "ORP":227.00, "TDS":162.46, "Turp": 249.23},{"Conductivity":1.54, "PH":9.30, "ORP":295.00, "TDS":162.46, "Turp": 232.04},{"Conductivity":1.57, "PH":9.23, "ORP":144.00, "TDS":162.46, "Turp": 232.04},{"Conductivity":1.54, "PH":9.14, "ORP":198.00, "TDS":162.46, "Turp": 232.04},{"Conductivity":1.57, "PH":9.19, "ORP":198.00, "TDS":162.46, "Turp": 232.04},{"Conductivity":1.54, "PH":9.14, "ORP":154.00, "TDS":162.46, "Turp": 232.04},{"Conductivity":1.57, "PH":9.19, "ORP":286.00, "TDS":162.46, "Turp": 232.04},{"Conductivity":1.57, "PH":9.25, "ORP":222.00, "TDS":162.46, "Turp": 232.04},{"Conductivity":1.57, "PH":9.25, "ORP":266.00, "TDS":162.46, "Turp": 232.04},{"Conductivity":1.54, "PH":9.30, "ORP":281.00, "TDS":162.46, "Turp": 232.04},{"Conductivity":1.54, "PH":9.23, "ORP":222.00, "TDS":162.46, "Turp": 232.04},{"Conductivity":1.54, "PH":9.23, "ORP":208.00, "TDS":162.46, "Turp": 232.04},{"Conductivity":1.54, "PH":9.18, "ORP":139.00, "TDS":162.46, "Turp": 232.04}]}'
                
        return json.loads(data) 
        
def normalizeDataSet(dataSet):
    cp_data  = dataSet
    
    for data in cp_data:
        mean = sum(data.values()) / len(data.values())
        std = np.std(list(data.values()))
        for k,v in data.items():
            data[k] = (v - mean) / std
        
    return cp_data

   
def main():
    print("Your actions are 0 for loading latest data set from output file and adding to model \n or 1 for querying a data point from the output file")
    action = int(input())
    if(action == 0):
        data = openLatestOutput()
        absolute = data[list(data.keys())[0]]
        center_point_absolute = centerPoint(absolute)
        closest_point_absolute = closestPoint(absolute)
        standards_absolute = standard_dev_cluster(absolute, center_point_absolute)
        ##for our absolute samples
        final_obj = {}
        final_obj = {
                    "timeStamp": datetime.datetime.today().strftime('%Y-%m-%d'),
                    "desc" : 'Tap water',
                    "contaminated" : 0,
                    "results" : data[list(data.keys())[0]],
                    "closest_point" : closest_point_absolute,
                    "center_point"  : center_point_absolute,
                    'standard_deviation': standards_absolute
                }
        addToModel(final_obj, "tap_water_absolute.json")
        normalized_data = normalizeDataSet(data[list(data.keys())[0]])
        
        
        center_point = centerPoint(normalized_data)
        closest_point = closestPoint(normalized_data)
        standards = standard_dev_cluster(normalized_data, center_point)
     
        final_obj = {}
        final_obj = {
                    "timeStamp": datetime.datetime.today().strftime('%Y-%m-%d'),
                    "desc" : 'Tap water',
                    "contaminated" : 0,
                    "results" : data[list(data.keys())[0]],
                    "closest_point" : closest_point,
                    "center_point"  : center_point,
                    'standard_deviation': standards
                }
        addToModel(final_obj)
        
        pprint("Done!")
    elif(action == 1):
        query = {'Conductivity': -0.8729087463837244, 'PH': -0.8448048541963021, 'ORP': 1.8116158462914003, 'TDS': -0.3918962550174805, 'Turp': 0.2979940093061065}
        print(queryPoint(query))
        testAccuracy()
        
        pprint("Done!")

main()
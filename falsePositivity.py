#!/usr/bin/python3

#Author: armins@bu.edu

import sys
import os
import json
import math
import numpy as np

""" 
    # Primary object of this script is to take two models
    # a testing model and a query model and check how similar the two
    # models are. We will accomplish this by iterating every cluster and every point of the 
    # query model and testing if and how many clusters those the query point land in the testing model
"""

def get_normalized_center(data_set, center_point):
    #this function could be redundant
    new_center_point = {}
    for k,v in center_point.items():
        seq = [x[k] for x in data_set["results"]]
        new_center_point[k] = (v - min(seq)) / (max(seq) - min(seq))

def standard_dev_cluster(data_set, center_point, dims = 5):
    #we first need to normalize before taking a mean center
    #mean_center = get_normalized_center(data_set, center_point)
    keys = ['Conductivity', 'PH', 'ORP', 'TDS', 'Turp']
    standard_devs = {}
    for i in range(0, dims):
        print(data_set.values())
        t1 = [list(data_set["results"])[i] for j in range(0, len(data_set["results"]))]
        t1 = []
        for j in range(0, len(data_set["results"])):
            t1.append(data_set["results"][i])

        mean_t1 = list(center_point.values())[i]
        rsum = 0.0
        for el in t1:
            rsum += math.pow(el - mean_t1, 2)
            
        standard_devs[keys[i]] = math.sqrt(rsum / (dims - 1))
    return standard_devs


def query_std(data_set, query_point):
    alpha = 20
    data_set_cp = data_set
    #Add a query to a data set
    old_std = data_set_cp["standard_deviation"]
    data_set_cp["results"].append(query_point)
    #Derive new standard deviation
    new_std = standard_dev_cluster(data_set_cp, data_set_cp["center_point"])
    #check if difference is greater than our standard
    return old_std - new_std > alpha

def test_against_models(testing_models, query_point):
    total = 0
    for test in testing_models:
        file_name = list(test.keys())[0]
        for exp in test[file_name]["Exps"]:
            total += 1 if query_std(exp, query_point) else 0 

    return total

if __name__ == "__main__":

    testing_model_dir = sys.argv[1] #expecting  a directory name
    query_model_dir = sys.argv[2] #expecting a directory name
    testing_models = []
    query_models = []

    for filename in os.listdir(query_model_dir):
        if("_norm" in filename): continue
        f = open(query_model_dir + '/' + filename, 'r')
        query_models.append({filename: json.loads(f.read())})

    for filename in os.listdir(testing_model_dir):
        if("_norm" in filename): continue
        f = open(testing_model_dir + '/' + filename, 'r')
        testing_models.append({filename: json.loads(f.read())})

    #Iterate through each query data point

    for test in query_models:
        file_name = list(test.keys())[0]
        print("===================== Testing %s ===================== " % file_name)
        total_results = 0
        total_in = 0
        exp_num = 0
        for exp in test[file_name]["Exps"]:
            total_results += len(exp["results"]) * len(testing_models)
            for query_point in exp["results"]:
                #on average how many testing models did this point land in 
                total_in += test_against_models(testing_models, query_point)
            
            print("++++++++++++++++++++++ Experiment number %d avg number of points that have landed in a testing models %d ++++++++++++++++++++++" %exp_num, total_in/total_results )
            exp_num += 1

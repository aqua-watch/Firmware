#!/usr/bin/python3

#Author: armins@bu.edu

import sys
import os
import json
from model import standard_dev_cluster


""" 
    # Primary object of this script is to take two models
    # a testing model and a query model and check how similar the two
    # models are. We will accomplish this by iterating every cluster and every point of the 
    # query model and testing if and how many clusters those the query point land in the testing model
"""

def standard_dev_cluster(data_set, center_point, dims = 5):
    """
    # @param: array of dicts -> data points
    # @param: Pre computed center point of the prev param
    # @param: Number of dimensions repersented by a datapoint
    """
    #imported over from /model.py
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


def query_std(data_set, query_point):
    #Add a query to a data set
    data_set["results"].append(query_point)




if __name__ == "__main__":
    testing_model_dir = sys.argv[1] #expecting  a directory name
    query_model_dir = sys.argv[2] #expecting a directory name
    testing_models = []
    query_models = []

    for filename in os.listdir(query_model_dir):
        f = open(query_model_dir + '/' + filename, 'r')
        query_models.append({filename: json.loads(f.read())})

    for filename in os.listdir(testing_model_dir):
        f = open(testing_model_dir + '/' + filename, 'r')
        testing_models.append({filename: json.loads(f.read())})






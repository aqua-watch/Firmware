# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 13:42:37 2018

@author: Armin
"""
import matplotlib.patches as mpatches
from matplotlib import pyplot as plt
import json
import formatModels
import sklearn.manifold
import sklearn.metrics as metrics
import matplotlib
import numpy as np
import random


def random_color():
    return list(np.random.choice(range(256), size=3))
                 
def plot_all_clusters():
    model_df = formatModels.formatModel()
    X = model_df.drop(['Desc','Timestamp','Contaminated'], axis=1).values
    y = model_df['Contaminated']
    
    euclidean_dists = metrics.euclidean_distances(X)
    mds = sklearn.manifold.MDS(n_components=2, max_iter=3000, eps=1e-9, random_state=0,
                   dissimilarity="precomputed", n_jobs=1)
    
    fit = mds.fit(euclidean_dists)
    pos = fit.embedding_
    #colors = matplotlib.cm.rainbow(np.linspace(0, 1, len(X)))
    colors = [random_color() for _ in range(0, len(X) // 50)] #amount of data points dev by size of clusters
    color_idx = 0;
    for idx in range(0, len(X) - 50, 50):
        _ = plt.scatter(pos[:, 0][idx], pos[:, 1], s=8, edgecolor='k',  marker='o', color = colors[color_idx])
        color_idx += 1
    
    #A = plt.scatter(pos[:, 0], pos[:, 1], s=8, edgecolor='k',  marker='o', color = colors[0])

def center_plot():
    ys = [5,10,15,20,25,30,35,40,45,50,55,60]
    ph = []
    cond = []
    orp = []
    tds = []
    turp = []
    
    model = {}  
    with open('5_min_model_norm.json') as f:
        model = f.read().replace('\n', '')
        model = json.loads(model)
    exps = model["Exps"]
    
    for exp in exps:       
        ph.append(exp["center_point"]["PH"])
        cond.append(exp["center_point"]["Conductivity"])
        orp.append(exp["center_point"]["ORP"])
        tds.append(exp["center_point"]["TDS"])
        turp.append(exp["center_point"]["Turp"])
    
    plt.figure(1)
    plt.plot(ys, cond, '-', label='Conductivity')
    plt.plot(ys , ph, '--', label='Ph')
    plt.plot(ys, orp, ':', label='ORP')
    plt.plot( ys, tds, '--y', label='TDS')
    plt.plot(ys, turp, '--g', label='Turbidity');
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.title("Center Points")
    plt.ylabel("Normalized sensor measurement")
    plt.xlabel("Minutes after lead added")
    
    #Ph_patch = mpatches.Patch(color='orange', marker='--', label='Ph')
    
   # plt.legend()
    plt.draw()
    #plt.savefig('imgs/distilled_water_model_norm_means.png')
    plt.show()

def standard_deviation_plot():
    ys = [5,10,15,20,25,30,35,40,45,50,55,60]
    ph = []
    cond = []
    orp = []
    tds = []
    turp = []
    model = {}  
    with open('5_min_model_norm.json') as f:
        model = f.read().replace('\n', '')
        model = json.loads(model)
        
    exps = model["Exps"]
    for exp in exps:
        ph.append(exp["standard_deviation"]["PH"])
        cond.append(exp["standard_deviation"]["Conductivity"])
        orp.append(exp["standard_deviation"]["ORP"])
        tds.append(exp["standard_deviation"]["TDS"])
        turp.append(exp["standard_deviation"]["Turp"])
    
    plt.figure(1)
    plt.plot( ys,cond, '-', label='Conductivity')
    plt.plot( ys, ph, '--', label='Ph')
    plt.plot( ys, orp, ':', label='ORP')
    plt.plot( ys, tds, '--y', label='TDS')
    plt.plot( ys, turp, '--g', label='Turbidity');
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.title("Standard Deviations")
    plt.ylabel("Normalized sensor measurement")
    plt.xlabel("Minutes after lead added")
    
    plt.draw()
   # plt.savefig('imgs/distilled_water_model_norm_stds.png')
    plt.show()

def printPH():
    ys = [5,10,15,20,25,30,35,40,45,50,55,60]
    ph = []
     
    with open('5_min_model_absolute.json') as f:
        model = f.read().replace('\n', '')
        model = json.loads(model)
        
    exps = model["Exps"]
    for exp in exps:
        ph.append(exp["center_point"]["PH"])
        
    
    plt.figure(1)
    plt.plot( ys, ph, '--', label='Ph')
    
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.title("Average PH values")
    plt.ylabel("Absolute sensor measurement")
    plt.xlabel("Minutes after lead added")
    
    plt.draw()
    #plt.savefig('imgs/distilled_water_model_norm_stds.png')
    plt.show()

def printCond():
    ys = [5,10,15,20,25,30,35,40,45,50,55,60]
    measurments = []
     
    with open('5_min_model_absolute.json') as f:
        model = f.read().replace('\n', '')
        model = json.loads(model)
        
    exps = model["Exps"]
    for exp in exps:
        measurments.append(exp["center_point"]["Conductivity"])
        
    
    plt.figure(1)
    plt.plot( ys, measurments, '--', label='Conductivity')
    
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.title("Average conductivity values")
    plt.ylabel("Absolute sensor measurement")
    plt.xlabel("Minutes after lead added")
    
    plt.draw()
    #plt.savefig('imgs/distilled_water_model_norm_stds.png')
    plt.show()
    
def printORP():
    ys = [5,10,15,20,25,30,35,40,45,50,55,60]
    measurments = []
     
    with open('5_min_model_absolute.json') as f:
        model = f.read().replace('\n', '')
        model = json.loads(model)
        
    exps = model["Exps"]
    for exp in exps:
        measurments.append(exp["center_point"]["ORP"])
        
    
    plt.figure(1)
    plt.plot( ys, measurments, '--', label='ORP')
    
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.title("Average ORP values")
    plt.ylabel("Absolute sensor measurement")
    plt.xlabel("Minutes after lead added")
    
    plt.draw()
    #plt.savefig('imgs/distilled_water_model_norm_stds.png')
    plt.show()

def printTDS():
    ys = [5,10,15,20,25,30,35,40,45,50,55,60]
    measurments = []
     
    with open('5_min_model_absolute.json') as f:
        model = f.read().replace('\n', '')
        model = json.loads(model)
        
    exps = model["Exps"]
    for exp in exps:
        measurments.append(exp["center_point"]["TDS"])
        
    
    plt.figure(1)
    plt.plot( ys, measurments, '--', label='TDS')
    
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.title("Average TDS values")
    plt.ylabel("Absolute sensor measurement")
    plt.xlabel("Minutes after lead added")
    
    plt.draw()
    #plt.savefig('imgs/distilled_water_model_norm_stds.png')
    plt.show()

def printTurp():
    ys = [5,10,15,20,25,30,35,40,45,50,55,60]
    measurments = []
     
    with open('5_min_model_absolute.json') as f:
        model = f.read().replace('\n', '')
        model = json.loads(model)
        
    exps = model["Exps"]
    for exp in exps:
        measurments.append(exp["center_point"]["Turp"])
        
    
    plt.figure(1)
    plt.plot( ys, measurments, '--', label='Turb')
    
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.title("Average Turbidity values")
    plt.ylabel("Absolute sensor measurement")
    plt.xlabel("Minutes after lead added")
    
    plt.draw()
    #plt.savefig('imgs/distilled_water_model_norm_stds.png')
    plt.show()


printCond()
printPH()
printORP()
printTDS()
printTurp()
standard_deviation_plot()   
center_plot()
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 13:42:37 2018

@author: Armin
"""
import matplotlib.patches as mpatches
from matplotlib import pyplot as plt
import json


def center_plot():
    ys = [0,0,15,30,45,60,75,90,105,120]
    ph = []
    cond = []
    orp = []
    tds = []
    turp = []
    
    model = {}  
    with open('model.json') as f:
        model = f.read().replace('\n', '')
        model = json.loads(model)
        
    for exp in model["Exps"]:       
        ph.append(exp["center_point"]["PH"])
        cond.append(exp["center_point"]["Conductivity"])
        orp.append(exp["center_point"]["ORP"])
        tds.append(exp["center_point"]["TDS"])
        turp.append(exp["center_point"]["Turp"])
    
    plt.figure(1)
    plt.plot(ys, cond[0:-1], '-', label='Conductivity')
    plt.plot(ys , ph[0:-1], '--', label='Ph')
    plt.plot(ys, orp[0:-1], ':', label='ORP')
    plt.plot( ys, tds[0:-1], '--y', label='TDS')
    plt.plot(ys, turp[0:-1], '--g', label='Turbidity');
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.title("Center Points")
    plt.ylabel("Normalized sensor measurement")
    plt.xlabel("Minutes after lead added")
    
    #Ph_patch = mpatches.Patch(color='orange', marker='--', label='Ph')
    
   # plt.legend()
    plt.draw()
    plt.savefig('ex1.png')
    plt.show()

def standard_deviation_plot():
    ys = [0,0,15,30,45,60,75,90,105,120]
    ph = []
    cond = []
    orp = []
    tds = []
    turp = []
    model = {}  
    with open('model.json') as f:
        model = f.read().replace('\n', '')
        model = json.loads(model)
        
    for exp in model["Exps"]:
        ph.append(exp["standard_deviation"]["PH"])
        cond.append(exp["standard_deviation"]["Conductivity"])
        orp.append(exp["standard_deviation"]["ORP"])
        tds.append(exp["standard_deviation"]["TDS"])
        turp.append(exp["standard_deviation"]["Turp"])
    
    plt.figure(1)
    plt.plot( ys,cond[0:-1], '-', label='Conductivity')
    plt.plot( ys, ph[0:-1], '--', label='Ph')
    plt.plot( ys, orp[0:-1], ':', label='ORP')
    plt.plot( ys, tds[0:-1], '--y', label='TDS')
    plt.plot( ys, turp[0:-1], '--g', label='Turbidity');
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.title("Standard Deviations")
    plt.ylabel("Normalized sensor measurement")
    plt.xlabel("Minutes after lead added")
    
    plt.draw()
    plt.savefig('ex2.png')
    plt.show()

standard_deviation_plot()   
center_plot()
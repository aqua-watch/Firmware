# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 13:42:37 2018

@author: Armin
"""
import matplotlib.patches as mpatches
from matplotlib import pyplot as plt
import json


def center_plot():
    ys = [15,30,45,60,75,90,105]
    ph = []
    cond = []
    orp = []
    tds = []
    turp = []
    
    model = {}  
    with open('distilled_water_model_norm.json') as f:
        model = f.read().replace('\n', '')
        model = json.loads(model)
    exps = model["Exps"][4:]
    
    for exp in exps:       
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
    plt.savefig('imgs/distilled_water_model_norm_means.png')
    plt.show()

def standard_deviation_plot():
    ys = [15,30,45,60,75,90,105,120]
    ph = []
    cond = []
    orp = []
    tds = []
    turp = []
    model = {}  
    with open('distilled_water_model_norm.json') as f:
        model = f.read().replace('\n', '')
        model = json.loads(model)
        
    exps = model["Exps"][4:]
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
    plt.savefig('imgs/distilled_water_model_norm_stds.png')
    plt.show()

def printPH():
    ys = [0,0,0,15,30,45,60,75,90,105,120]
    ph = []
     
    with open('distilled_water_model_absolute.json') as f:
        model = f.read().replace('\n', '')
        model = json.loads(model)
        
    exps = model["Exps"]
    for exp in exps:
        ph.append(exp["center_point"]["PH"])
        
    
    plt.figure(1)
    plt.plot( ys, ph[0:-1], '--', label='Ph')
    
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.title("Average PH values")
    plt.ylabel("Absolute sensor measurement")
    plt.xlabel("Minutes after lead added")
    
    plt.draw()
    #plt.savefig('imgs/distilled_water_model_norm_stds.png')
    plt.show()

def printCond():
    ys = [0,0,0,15,30,45,60,75,90,105,120]
    measurments = []
     
    with open('distilled_water_model_absolute.json') as f:
        model = f.read().replace('\n', '')
        model = json.loads(model)
        
    exps = model["Exps"]
    for exp in exps:
        measurments.append(exp["center_point"]["Conductivity"])
        
    
    plt.figure(1)
    plt.plot( ys, measurments[0:-1], '--', label='Conductivity')
    
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.title("Average conductivity values")
    plt.ylabel("Absolute sensor measurement")
    plt.xlabel("Minutes after lead added")
    
    plt.draw()
    #plt.savefig('imgs/distilled_water_model_norm_stds.png')
    plt.show()
    
def printORP():
    ys = [0,0,0,15,30,45,60,75,90,105,120]
    measurments = []
     
    with open('distilled_water_model_absolute.json') as f:
        model = f.read().replace('\n', '')
        model = json.loads(model)
        
    exps = model["Exps"]
    for exp in exps:
        measurments.append(exp["center_point"]["ORP"])
        
    
    plt.figure(1)
    plt.plot( ys, measurments[0:-1], '--', label='ORP')
    
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.title("Average ORP values")
    plt.ylabel("Absolute sensor measurement")
    plt.xlabel("Minutes after lead added")
    
    plt.draw()
    #plt.savefig('imgs/distilled_water_model_norm_stds.png')
    plt.show()

def printTDS():
    ys = [0,0,0,15,30,45,60,75,90,105,120]
    measurments = []
     
    with open('distilled_water_model_absolute.json') as f:
        model = f.read().replace('\n', '')
        model = json.loads(model)
        
    exps = model["Exps"]
    for exp in exps:
        measurments.append(exp["center_point"]["TDS"])
        
    
    plt.figure(1)
    plt.plot( ys, measurments[0:-1], '--', label='TDS')
    
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.title("Average TDS values")
    plt.ylabel("Absolute sensor measurement")
    plt.xlabel("Minutes after lead added")
    
    plt.draw()
    #plt.savefig('imgs/distilled_water_model_norm_stds.png')
    plt.show()

def printTurp():
    ys = [0,0,0,15,30,45,60,75,90,105,120]
    measurments = []
     
    with open('distilled_water_model_absolute.json') as f:
        model = f.read().replace('\n', '')
        model = json.loads(model)
        
    exps = model["Exps"]
    for exp in exps:
        measurments.append(exp["center_point"]["Turp"])
        
    
    plt.figure(1)
    plt.plot( ys, measurments[0:-1], '--', label='Turb')
    
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
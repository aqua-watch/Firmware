# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 13:42:37 2018

@author: Armin
"""
import matplotlib.patches as mpatches
from matplotlib import pyplot as plt


def center_plot():
    ys = [0, 1, 2, 23, 504]
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
    #cond = [-0.7893437821450888,-1.0891302435242785, -0.8989975182534178, -1.140448307938395]
    #ph = [-0.7052077335593695,-1.0578289294875156, -0.8699537275687201, -1.1120866361712134]
    #orp = [0.28235349140898075, 1.3473773744780033, 1.755265030810739, 1.4269126262363487]
    #tds = [-0.5661405487071837, -0.08584349015095687, -0.39622690231585284, 0.34291023996117187]
    #turp = [1.845718023990502, 0.8854252886847475, 0.4099131173272524, 0.4827120779120873] 
    
    
    plt.figure(1)
    plt.plot(cond, ys, '-', label='Conductivity')
    plt.plot( ph, ys, '--', label='Ph')
    plt.plot(orp, ys, ':', label='ORP')
    plt.plot( tds, ys, '--y', label='TDS')
    plt.plot(turp, ys, '--g', label='Turbidity');
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.title("Center Points")
    plt.ylabel("Hours after lead added")
    plt.xlabel("Normalized sensor measurement")
    
    #Ph_patch = mpatches.Patch(color='orange', marker='--', label='Ph')
    
   # plt.legend()
    plt.draw()
    plt.savefig('ex1.png')
    plt.show()

def standard_deviation_plot():
    ys = [0, 1, 2, 23, 504]
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
    plt.plot(cond, ys, '-', label='Conductivity')
    plt.plot( ph, ys, '--', label='Ph')
    plt.plot(orp, ys, ':', label='ORP')
    plt.plot( tds, ys, '--y', label='TDS')
    plt.plot(turp, ys, '--g', label='Turbidity');
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.title("Standard Deviations")
    plt.ylabel("Hours after lead added")
    plt.xlabel("Normalized sensor measurement")
    
    plt.draw()
    plt.savefig('ex2.png')
    plt.show()

standard_deviation_plot()   
center_plot()
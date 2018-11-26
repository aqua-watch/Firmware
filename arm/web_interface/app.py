# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from flask import Markup

import json
import sys
sys.path.insert(0, '../../')
from formatModels import get_absolute_values
from formatModels import get_normalized_values
from formatModels import get_normalized_values_json
from formatModels import get_absolute_values_json
#sys.path.append('arm/web_interface/')

app = Flask(__name__)

@app.route('/', methods=['GET'])
def display_content():
    
    norm_df = get_normalized_values()
    absolute_df = get_absolute_values()
    
    contaminated_norm = norm_df[norm_df.Contaminated >= 1]
    contaminated_abs = absolute_df[absolute_df.Contaminated >= 1]
    
    norm_json = get_normalized_values_json()
    abs_json = get_absolute_values_json()
            
    times = []
    
    i = 5
    for _ in range(0, int(len(contaminated_abs) / 50)):
        times.append(i)
        i += 5
        
    ##### For normalized #####
    norm_ph = []
    norm_cond = []
    norm_orp = []
    norm_tds = []
    norm_turp = []
    
    norm_ph_std = []
    norm_cond_std = []
    norm_orp_std = []
    norm_tds_std = []
    norm_turp_std = []

    exps = norm_json["Exps"]
    
    for exp in exps:
        if(exp["contaminated"] == 1): 
            norm_ph.append(exp["center_point"]["PH"])
            norm_cond.append(exp["center_point"]["Conductivity"])
            norm_orp.append(exp["center_point"]["ORP"])
            norm_tds.append(exp["center_point"]["TDS"])
            norm_turp.append(exp["center_point"]["Turp"])    
            
            norm_ph_std.append(exp["standard_deviation"]["PH"])
            norm_cond_std.append(exp["standard_deviation"]["Conductivity"])
            norm_orp_std.append(exp["standard_deviation"]["ORP"])
            norm_tds_std.append(exp["standard_deviation"]["TDS"])
            norm_turp_std.append(exp["standard_deviation"]["Turp"])  
    
    norm_html = Markup(norm_df.to_html())
    absolute_html = Markup(absolute_df.to_html())
    
    
    
    return render_template('content.html', normalized=norm_html, absolute=absolute_html, 
                           times=json.dumps(times),
                           norm_ph=norm_ph,
                           norm_cond=norm_cond,
                           norm_orp=norm_orp,
                           norm_tds=norm_tds,
                           norm_turp=norm_turp,
                           norm_ph_std=norm_ph_std,
                           norm_cond_std=norm_cond_std,
                           norm_orp_std=norm_orp_std,
                           norm_tds_std=norm_tds_std,
                           norm_turp_std=norm_turp_std,
                           ) 
    
    
    
    
    
    
    
    
# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from flask import Markup


import sys
sys.path.insert(0, '../../')
from formatModels import get_absolute_values
from formatModels import get_normalized_values
#sys.path.append('arm/web_interface/')

app = Flask(__name__)

@app.route('/', methods=['GET'])
def display_content():
    
    norm_df = get_normalized_values()
    absolute_df = get_absolute_values()
    
    
    norm_html = Markup(norm_df.to_html())
    absolute_html = Markup(absolute_df.to_html())
    
    
    
    return render_template('content.html', normalized=norm_html, absolute=absolute_html) 
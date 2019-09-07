# -*- coding: utf-8 -*-
#/src/views/HomeView.py
"""
                     Api Auto complete 
    ------------------------------------------------------------------------
                        Home
    ------------------------------------------------------------------------
    
    URLs: https://flask.palletsprojects.com/en/1.1.x/
  

"""
from quart import request, g, Blueprint, json, render_template

home_api = Blueprint('home_api', __name__)

@home_api.route('/', methods=['GET','POST'])
async def index():
    """
    Home
    """
    return await render_template('index.html')
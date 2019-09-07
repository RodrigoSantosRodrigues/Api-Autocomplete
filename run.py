# -*- coding: utf-8 -*-
# encoding: utf-8
# /run.py
"""
                      Api Auto complete
    ------------------------------------------------------------------------
                        Initialize developer server 
    ------------------------------------------------------------------------
    
    URLs: https://flask.palletsprojects.com/en/1.1.x/
       


"""
import os
from dotenv import load_dotenv, find_dotenv

from src.app import create_app

load_dotenv(find_dotenv())

env_name = os.getenv('FLASK_ENV')
app = create_app(env_name)

if __name__ == '__main__':
  port = os.getenv('APP_PORT')
  host = os.getenv('APP_HOST')
  # run app
  app.run(host=host, port=port)

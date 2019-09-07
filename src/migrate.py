# -*- coding: utf-8 -*-
# src / app.py
"""
                    Api Auto complete
    ------------------------------------------------------------------------
                        App de migração
    ------------------------------------------------------------------------
    
    URLs: https://flask.palletsprojects.com/en/1.1.x/
      

"""
from flask import Flask
from .config import app_config
from .models import db, bcrypt



def create_app(env_name):
  # app initiliazation with Flask
  APP = Flask(__name__)

  APP.config.from_object(app_config[env_name])

  # initializing bcrypt and db
  bcrypt.init_app(APP)
  db.init_app(APP)

  return APP
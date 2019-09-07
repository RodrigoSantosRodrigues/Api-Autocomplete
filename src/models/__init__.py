# -*- coding: utf-8 -*-
#src/models/__init__.py
"""
                     Api Auto complete 
    ------------------------------------------------------------------------
                        __init__
    ------------------------------------------------------------------------
    
    URLs: https://flask.palletsprojects.com/en/1.1.x/
          https://docs.sqlalchemy.org/en/13/
    
"""
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# initialize db
db = SQLAlchemy()
bcrypt = Bcrypt()

from .UserModel import UserModel, UserSchema
from .EntityModel import EntityModel, EntitySchema
from .CollectorModel import CollectorModel, CollectorSchema
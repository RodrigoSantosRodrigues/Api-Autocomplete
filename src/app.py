# -*- coding: utf-8 -*-
# src / app.py
"""
                    Api Auto complete
    ------------------------------------------------------------------------
                        App
    ------------------------------------------------------------------------
    
    URLs: https://flask.palletsprojects.com/en/1.1.x/
      

"""
import quart.flask_patch

from .config import app_config
from .models import db, bcrypt

from .views.UserView import user_api as user_blueprint
from .views.EntityView import entity_api as entity_blueprint
from .views.CollectorView import collector_api as collector_blueprint
from .views.AutoCompleteView import autocomplete_api as autocomplete_blueprint
from .views.HomeView import home_api as home_blueprint

from flask_swagger_ui import get_swaggerui_blueprint

from quart import Quart
from quart_cors import cors



def create_app(env_name):
  """
    param: env_name -> necessário para carregar nossa configuração no modo development ou production

    DOC API USING SWAGGER UI  
    Create app
  """
  
  # app initiliazation
  APP = Quart(__name__)
  APP = cors(APP, allow_origin="*")

  APP.config.from_object(app_config[env_name])

  # initializing bcrypt and db
  bcrypt.init_app(APP)
  db.init_app(APP)

  ### swagger specific ###
  SWAGGER_URL = '/apidocs'
  API_URL = '/static/api/openapi.json'
  SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Auto Complete Service"
    }
  )
  APP.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
  ### end swagger specific ###

  APP.register_blueprint(user_blueprint, url_prefix='/api/users')
  APP.register_blueprint(entity_blueprint, url_prefix='/api/entities')
  APP.register_blueprint(collector_blueprint, url_prefix='/api/collectors')
  APP.register_blueprint(autocomplete_blueprint, url_prefix='/api/autocompleties')
  APP.register_blueprint(home_blueprint, url_prefix='')

  return APP
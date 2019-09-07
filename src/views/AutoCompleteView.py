# -*- coding: utf-8 -*-
#/src/views/EntityView.py
"""
                     Api Auto complete 
    ------------------------------------------------------------------------
                        Auto Complete
    ------------------------------------------------------------------------
    
    URLs: https://flask.palletsprojects.com/en/1.1.x/
  
"""

from quart import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..predict.AutoComplete import Complete

autocomplete_api = Blueprint('autocomplete_api', __name__)


@autocomplete_api.route('/', methods=['POST'])
@Auth.auth_required
async def autocomplete():
  """
  Create Auto Complete
   ---
  /api/autocompleties/:
    post:
      summary: "Auto completar"
      security:
        - APIKeyHeader: []
      tags:
        - AutoComplete
      requestBody:
        description: Funções de auto complete
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - letters
              properties:
                letters:
                  type: string
      responses:
        '200':
          description: Sucesso
        '400':
          description: "Erro ao auto completar"
  """
  req_data = await request.get_json()

  word = await Complete.completing(req_data.get('letters'))

  return custom_response(word, 200)





def custom_response(res, status_code):
  """
  Custom Response Function
  """
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )


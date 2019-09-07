# -*- coding: utf-8 -*-
#/src/views/EntityView.py
"""
                     Api Auto complete 
    ------------------------------------------------------------------------
                        Events Collector
    ------------------------------------------------------------------------
    
    URLs: https://flask.palletsprojects.com/en/1.1.x/
  
"""

from quart import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.CollectorModel import CollectorModel, CollectorSchema
from ..models.UserModel import UserModel, UserSchema

collector_api = Blueprint('collector_api', __name__)
collector_schema = CollectorSchema()
UserSchema = UserSchema()


@collector_api.route('/', methods=['POST'])
@Auth.auth_required
async def create():
  """
   ---
  /api/collectors/:
    post:
      summary: Criar um evento.
      security:
        - APIKeyHeader: []
      tags:
        - Collector
      requestBody:
        description: Funções de eventos
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - event
                - timestamp
              properties:
                event:
                  type: string
                timestamp:
                  type: string
      responses:
        '200':
          description: Evento criado com sucesso
        '400':
          description: Dados ausentes
  """
  req_data = await request.get_json()
  
  req_data['owner_id'] = g.user.get('id')
  data, error = collector_schema.load(req_data)
  if error:
    return custom_response(error, 400)
  
  post = CollectorModel(data)
  await post.save()
  data = collector_schema.dump(post).data
  return custom_response(data, 200)




@collector_api.route('/<int:event_id>', methods=['GET'])
@Auth.auth_required
async def get_one(event_id):
  """
  ---
  /api/collectors/{event_id}:
    get:
      summary: Buscar um evento pelo ID
      security:
        - APIKeyHeader: []
      tags:
        - Collector
      parameters:
        - in: path
          name: event_id
          required: true
          schema:
            type: integer
            minimum: 1
            description: ID de um evento

      responses:
        '200':
          description: Dados retornados com sucesso
        '400':
          description: Evento não existe
        '401':
          description: Permissão de acesso negado
  """
  post = await CollectorModel.get_one_event(event_id)
  if not post:
    return custom_response({'error': 'post not found'}, 400)
  data = collector_schema.dump(post).data

  if g.user.get('id') != data.get('owner_id'):
    return custom_response({'error': 'permission denied'}, 401)

  return custom_response(data, 200)



@collector_api.route('/', methods=['GET'])
@Auth.auth_required
async def get_all():
  """
  --- 
  /api/collectors/:
    get:
      summary: Buscar todas os eventos. Você deve ser um administrador para acessar esse recurso
      security:
        - APIKeyHeader: []
      tags:
        - Collector
      
      responses:
        '200':
          description: Retorna todas os eventos com sucesso
        '400':
          description: Não existe eventos
        '401':
          description: Permissão de acesso negado
  """
  post_user= await UserModel.get_one_user(g.user.get('id'))
  if not post_user:
    return custom_response({'error': 'user not found'}, 400)
  data_user= UserSchema.dump(post_user).data
 
  if data_user.get('role') != 'Admin':
    return custom_response({'error': 'permission denied'}, 401)

  posts = await CollectorModel.get_all_events()
  data = collector_schema.dump(posts, many=True).data
  return custom_response(data, 200)




def custom_response(res, status_code):
  """
  Custom Response Function
  """
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )


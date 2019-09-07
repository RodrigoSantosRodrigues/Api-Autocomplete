# -*- coding: utf-8 -*-
#/src/views/EntityView.py
"""
                     Api Auto complete 
    ------------------------------------------------------------------------
                        Entities
    ------------------------------------------------------------------------
    
    URLs: https://flask.palletsprojects.com/en/1.1.x/
  
"""

from quart import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.EntityModel import EntityModel, EntitySchema
from ..models.UserModel import UserModel, UserSchema

entity_api = Blueprint('entity_api', __name__)
entity_schema = EntitySchema()
UserSchema = UserSchema()



@entity_api.route('/', methods=['POST'])
@Auth.auth_required
async def create():
  """
  Create Entity Function
   ---
  /api/entities/:
    post:
      summary: Criar uma entidade.
      security:
        - APIKeyHeader: []
      tags:
        - Entity
      requestBody:
        description: Funções de entidade
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - name
                - documento
              properties:
                name:
                  type: string
                documento:
                  type: string
      responses:
        '200':
          description: Entidade criado com sucesso
        '400':
          description: Dados ausentes
        '401':
          description: Documento informado já exite
        '402':
          description: Já existe uma conta para esse usuário

  """
  req_data = await request.get_json()
  
  req_data['owner_id'] = g.user.get('id')
  data, error = entity_schema.load(req_data)
  if error:
    return custom_response(error, 400)
  
  document_in_db = await EntityModel.get_entity_by_documento(req_data.get('documento'))
  if document_in_db:
    print(document_in_db)
    message = {'error': 'Document already exists for this user, please supply another document'}
    return custom_response(message, 401)

  user_in_db = await EntityModel.get_entity_by_user(data.get('owner_id'))
  if user_in_db:
    message = {'error': 'There is already a registration for this user'}
    return custom_response(message, 402)
  
  post = EntityModel(data)
  await post.save()
  data = entity_schema.dump(post).data
  return custom_response(data, 200)






@entity_api.route('/', methods=['GET'])
@Auth.auth_required
async def get_all():
  """
  Get All Entitys
  --- 
  /api/entities/:
    get:
      summary: Buscar todas as entidades. Você deve ser um administrador para acessar esse recurso
      security:
        - APIKeyHeader: []
      tags:
        - Entity
      
      responses:
        '200':
          description: Retorna todas as entidades com sucesso
        '400':
          description: Não existe entidades
        '401':
          description: Permissão de acesso negado
  """
  post_user= await UserModel.get_one_user(g.user.get('id'))
  if not post_user:
    return custom_response({'error': 'user not found'}, 400)
  data_user= UserSchema.dump(post_user).data
 
  if data_user.get('role') != 'Admin':
    return custom_response({'error': 'permission denied'}, 401)

  posts = await EntityModel.get_all_Entities()
  data = entity_schema.dump(posts, many=True).data
  return custom_response(data, 200)







@entity_api.route('/<int:entity_id>', methods=['GET'])
@Auth.auth_required
async def get_one(entity_id):
  """
  Get A Entity
  ---
  /api/entities/{entity_id}:
    get:
      summary: Buscar uma entidade pelo ID
      security:
        - APIKeyHeader: []
      tags:
        - Entity
      parameters:
        - in: path
          name: entity_id
          required: true
          schema:
            type: integer
            minimum: 1
            description: ID de uma entidade

      responses:
        '200':
          description: Dados retornados com sucesso
        '400':
          description: Entidade não existe
        '401':
          description: Permissão de acesso negado
  """
  post = await EntityModel.get_one_entity(entity_id)
  if not post:
    return custom_response({'error': 'post not found'}, 400)
  data = entity_schema.dump(post).data

  if g.user.get('id') != data.get('owner_id'):
    return custom_response({'error': 'permission denied'}, 401)

  return custom_response(data, 200)








@entity_api.route('/<int:entity_id>', methods=['PUT'])
@Auth.auth_required
async def update(entity_id):
  """
  Update A Entity
  ---
  /api/entities/{entity_id}:
    put:
      summary: Atualizar uma entidade
      security:
        - APIKeyHeader: []
      tags:
        - Entity
      parameters:
        - in: path
          name: entity_id
          required: true
          schema:
            type: integer
            minimum: 1
            description: ID de uma entidade
      requestBody:
        description: Funções de uma entidade
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - name
                - documento
              properties:
                name:
                  type: string
                documento:
                  type: string
      responses:
        '200':
          description: Entidade atualizado com sucesso
        '400':
          description: Entidade não existe
        '401':
          description: Permissão de acesso negado
        '402':
          description: Dados ausentes
        '403':
          description: Documento já existe, por favor, informe um documento válido

  """
  req_data = await request.get_json()
  post = await EntityModel.get_one_entity(entity_id)
  if not post:
    return custom_response({'error': 'entity not found'}, 400)
  data_entity = entity_schema.dump(post).data

  if data_entity.get('owner_id') != g.user.get('id'):
    return custom_response({'error': 'permission denied'}, 401)
  
  data, error = entity_schema.load(req_data, partial=True)
  if error:
    return custom_response(error, 402)

  if req_data.get('documento'):
    if req_data.get('documento') != data_entity.get('documento'):
      document_in_db = await EntityModel.get_entity_by_documento(data.get('documento'))
      if document_in_db:
        message = {'error': 'Document already exists for this user, please supply another document'}
        return custom_response(message, 403)
  
  await post.update(data)
  data = entity_schema.dump(post).data
  return custom_response(data, 200)









@entity_api.route('/<int:entity_id>', methods=['DELETE'])
@Auth.auth_required
async def delete(entity_id):
  """
  Delete A Entity
  ---
  /api/entities/{entity_id}:
    delete:
      summary: Deletar uma entidade
      security:
        - APIKeyHeader: []
      tags:
        - Entity
      parameters:
        - in: path
          name: entity_id
          required: true
          schema:
            type: integer
            minimum: 1
            description: ID de uma entidade
      responses:
        '200':
          description: Entidade deletado com sucesso
        '400':
          description: Entidade não existe
        '401':
          description: Permissão de acesso negado
  """
  post = await EntityModel.get_one_entity(entity_id)
  if not post:
    return custom_response({'error': 'entity not found'}, 400)
  data = entity_schema.dump(post).data
  if data.get('owner_id') != g.user.get('id'):
    return custom_response({'error': 'permission denied'}, 401)

  await post.delete()
  return custom_response({'message': 'deleted'}, 200)


  




def custom_response(res, status_code):
  """
  Custom Response Function
  """
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )


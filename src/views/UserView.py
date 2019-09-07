# -*- coding: utf-8 -*-
#/src/views/UserView
"""
                     Api Auto complete 
    ------------------------------------------------------------------------
                        Users
    ------------------------------------------------------------------------
    
    URLs: https://flask.palletsprojects.com/en/1.1.x/
  
"""

from quart import request, json, Response, Blueprint, g
from ..models.UserModel import UserModel, UserSchema
from ..shared.Authentication import Auth


user_api = Blueprint('user_api', __name__) 
user_schema = UserSchema()




@user_api.route('/', methods=['POST'])
async def create():
  """
  

  Create User Function
  --- 
  /api/users/:
    post:
      summary: Criar usuário. Retorna um jwt-token para autenticação no serviço
      tags:
        - User
      requestBody:
        description: Usuários
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - name
                - email
                - password
                - role
              properties:
                name:
                  type: string
                email:
                  type: string
                password:
                  type: string
                role:
                  type: string
  
      responses:
        '200':
          description: Usuário registrado com sucesso
        '400':
          description: Usuário já existe, por favor, informe um email diferente

  """
  req_data = await request.get_json() 
  
  data, error = user_schema.load(req_data)
  if error:
    return custom_response(error, 400)
 
  user_in_db = await UserModel.get_user_by_email(data.get('email'))
  if user_in_db:
    message = {'error': 'User already exist, please supply another email address'}
    return custom_response(message, 400)
  
  user = UserModel(data)
  await user.save()
  ser_data = user_schema.dump(user).data

  token = Auth.generate_token(ser_data.get('id'))
  return custom_response({'jwt_token': token}, 200)







@user_api.route('/', methods=['GET'])
@Auth.auth_required
async def get_all():
  """
  Get all users
   --- 
  /api/users/:
    get:
      summary: Buscar todos os usuários
      security:
        - APIKeyHeader: []
      tags:
        - User
      
      responses:
        '200':
          description: Retorna todos os usuários com sucesso
        '400':
          description: Usuário não existe
        '401':
          description: Permissão de acesso negado
  """
  user_id = g.user.get('id')
 
  post_user= await UserModel.get_one_user(user_id)
  if not post_user:
    return custom_response({'error': 'user not found'}, 400)
  data_user= user_schema.dump(post_user).data

  if data_user.get('role') != 'Admin':
    return custom_response({'error': 'permission denied'}, 401)

  users = await UserModel.get_all_users()
  ser_users = user_schema.dump(users, many=True).data
  return custom_response(ser_users, 200)






@user_api.route('/<int:user_id>', methods=['GET'])
@Auth.auth_required
async def get_a_user(user_id):
  """
  Get a single user
  ---
  /api/users/{user_id}:
    get:
      summary: Buscar um usuário pelo ID
      security:
        - APIKeyHeader: []
      tags:
        - User
      parameters:
        - in: path
          name: user_id
          required: true
          schema:
            type: integer
            minimum: 1
            description: ID de usuário

      responses:
        '200':
          description: Dados de usuário retornados com sucesso
        '400':
          description: Usuário não existe
        '401':
          description: Permissão de acesso negado
  """
  user = await UserModel.get_one_user(user_id)
  if not user:
    return custom_response({'error': 'user not found'}, 400)
  data = user_schema.dump(user).data

  if data.get('role') != 'Admin':
    return custom_response({'error': 'permission denied'}, 401)
  
  return custom_response(data, 200)







@user_api.route('/me', methods=['PUT'])
@Auth.auth_required
async def update():
  """
  Update me
  ---
    put:
      summary: Atuaizar dados de usuário existente
      security:
        - APIKeyHeader: []
      tags:
        - User
      requestBody:
        description: Funções de usuários
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - name
                - email
                - password
                - role
              properties:
                name:
                  type: string
                email:
                  type: string
                password:
                  type: string
                role:
                  type: string
      responses:
        '200':
          description: Usuário atualizado com sucesso
        '400':
          description: Dados faltantes
  """
  req_data = await request.get_json()
  data, error = user_schema.load(req_data, partial=True)
  if error:
    return custom_response(error, 400)

  user = await UserModel.get_one_user(g.user.get('id'))
  await user.update(data)
  ser_user = user_schema.dump(user).data
  return custom_response(ser_user, 200)






@user_api.route('/me', methods=['DELETE'])
@Auth.auth_required
async def delete():
  """
  Delete a user
  ---
  /api/users/me:
    delete:
      summary: Deletar usuário logado
      security:
        - APIKeyHeader: []
      tags:
        - User
      responses:
        '200':
          description: Usuário deletado com sucesso
  """
  user = await UserModel.get_one_user(g.user.get('id'))
  await user.delete()
  return custom_response({'message': 'deleted'}, 200)








@user_api.route('/me', methods=['GET'])
@Auth.auth_required
async def get_me():
  """
  Get me
  ---
  /api/users/me:
    get:
      summary: Retorna seus dados
      security:
        - APIKeyHeader: []
      tags:
        - User
      responses:
        '200':
          description: Dados buscados com sucesso
        '400':
          description: Erro ao consultar dados
  """
  user = await UserModel.get_one_user(g.user.get('id'))
  ser_user = user_schema.dump(user).data
  return custom_response(ser_user, 200)








@user_api.route('/login', methods=['POST'])
async def login():
  """
  User Login Function
  ------
  /api/users/login:
    post:
      summary: Realizar login na api, retorna um token de autenticação
      tags:
        - User
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                email:
                  type: string
                password:
                  type: string
      responses:
        '200':
          description: Login realizado com sucesso, token retornado com sucesso
        '400':
          description: Dados ausentes
        '401':
          description: Informe um email válido e uma senha válida
        '402':
          description: Credenciais inválidas
        '403':
          description: Credenciais inválidas
  """
  req_data = await request.get_json() 

  data, error = user_schema.load(req_data, partial=True) 
  if error:
    return custom_response(error, 400)

  if not data.get('email') or not data.get('password'):
    return custom_response({'error': 'you need email and password to sign in'}, 401)

  user = await UserModel.get_user_by_email(data.get('email'))
  if not user:
    return custom_response({'error': 'invalid credentials'}, 402)

  if not user.check_hash(data.get('password')):
    return custom_response({'error': 'invalid credentials'}, 403)

  ser_data = user_schema.dump(user).data
  token = Auth.generate_token(ser_data.get('id'))
  return custom_response({'jwt_token': token}, 200)

  



def custom_response(res, status_code):
  """
  Custom Response Function
  """
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )

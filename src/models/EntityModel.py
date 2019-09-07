# -*- coding: utf-8 -*-
# src/models/EntityModel.py
"""
                         Api Auto complete
    ------------------------------------------------------------------------
                        Modelo de Entity
    ------------------------------------------------------------------------
    
    URLs: https://flask.palletsprojects.com/en/1.1.x/
          https://docs.sqlalchemy.org/en/13/
          https://marshmallow.readthedocs.io/en/stable/
    
"""
from marshmallow import fields, Schema
import datetime
from . import db, bcrypt

class EntityModel(db.Model):
  """
  User Entity
  """

  # table name
  __tablename__ = 'entities'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), nullable=False)
  documento = db.Column(db.String(128), nullable=False, unique=True)
  created_at = db.Column(db.DateTime)
  modified_at = db.Column(db.DateTime)
  owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
 
  def __init__(self, data):
    """
    Class constructor
    """
    self.name= data.get('name')
    self.documento= data.get('documento')
    self.owner_id= data.get('owner_id')
    self.created_at = datetime.datetime.utcnow()
    self.modified_at = datetime.datetime.utcnow()

  async def save(self):
    db.session.add(self)
    db.session.commit()

  async def update(self, data):
    for key, item in data.items():
      setattr(self, key, item)
    self.modified_at = datetime.datetime.utcnow()
    db.session.commit()

  async def delete(self):
    db.session.delete(self)
    db.session.commit()
  
  @staticmethod
  async def get_all_Entities(): 
    return EntityModel.query.all()
  
  @staticmethod
  async def get_one_entity(id): 
    return EntityModel.query.filter_by(id=id).first()
  
  @staticmethod
  async def get_entity_by_user(owner_id):
    return EntityModel.query.filter_by(owner_id= owner_id).first()
  
  @staticmethod
  async def get_entity_by_documento(documento):
    return EntityModel.query.filter_by(documento= documento).first()
  

  """Métodos estáticos adicionais"""
  def __repr(self):
    return '<id {}>'.format(self.id)




class EntitySchema(Schema):
  id = fields.Int(dump_only=True)
  name= fields.Str(required=True)
  documento= fields.Str(required=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)
  owner_id = fields.Int(required=True)

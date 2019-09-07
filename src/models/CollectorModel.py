# -*- coding: utf-8 -*-
# src/models/ColletorModel.py
"""
                         Api Auto complete
    ------------------------------------------------------------------------
                        Modelo de Collector
    ------------------------------------------------------------------------
    
    URLs: https://flask.palletsprojects.com/en/1.1.x/
          https://docs.sqlalchemy.org/en/13/
          https://marshmallow.readthedocs.io/en/stable/
    
"""
from marshmallow import fields, Schema
import datetime
from . import db, bcrypt

class CollectorModel(db.Model):
  """
    Class Collector
  """

  # table name
  __tablename__ = 'collectors'

  id = db.Column(db.Integer, primary_key=True)
  event = db.Column(db.String(128), nullable=False)
  timestamp = db.Column(db.DateTime, nullable=True)
  created_at = db.Column(db.DateTime)
  modified_at = db.Column(db.DateTime)
  owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
 

  def __init__(self, data):
    """
    Class constructor
    """
    self.event= data.get('event')
    self.timestamp= data.get('timestamp')
    self.owner_id= data.get('owner_id')
    self.created_at = datetime.datetime.utcnow()
    self.modified_at = datetime.datetime.utcnow()


  async def save(self):
    db.session.add(self)
    db.session.commit()


  @staticmethod
  async def get_all_events(): 
    return CollectorModel.query.all()
  
  @staticmethod
  async def get_one_event(id):
    return CollectorModel.query.filter_by(id=id).first()
  
  @staticmethod
  async def get_event_by_user(owner_id):
    return CollectorModel.query.filter_by(owner_id= owner_id).all()
  


class CollectorSchema(Schema):
  id = fields.Int(dump_only=True)
  event= fields.Str(required=True)
  timestamp= fields.DateTime(required=False)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)
  owner_id = fields.Int(required=True)

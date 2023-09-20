#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import os
variable_name = 'HBNB_TYPE_STORAGE'
env_value = os.environ.get(variable_name)


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    if env_value == 'db':
        cities = relationship(
                'City', backref='states', cascade='all, delete-orphan')
    else:
        cities = self.link()

    def link(self):
        from models.__init__ import storage
        obj_list = []
        strg = storage.all(City)
        for value in strg:
            if self.id == value.state_id:
                obj_list.append(value)
        return obj_list

#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from models.city import City
from models import storage

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    
    name = Column(String(128), nullable=False)

    if os.environ.get('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship('City', backref='state')
    else:
        @property
        def cities(self):
            obj_list = []
            for city in storage.all(City).values():
                if self.id == city.state_id:
                    obj_list.append(city)
            return obj_list


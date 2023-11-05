#!/usr/bin/python3
"""Create the engine and database storage"""

import os
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

CLASSES = {"Amenity": Amenity, "City": City, "Place": Place, "Review": Review, "State": State, "User": User}

class DBStorage:
    """Database storage class for storing instances of models"""

    __engine = None
    __session = None

    def __init__(self):
        """Initialize the database engine"""
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                os.environ.get('HBNB_MYSQL_USER'),
                os.environ.get('HBNB_MYSQL_PWD'),
                os.environ.get('HBNB_MYSQL_HOST'),
                os.environ.get('HBNB_MYSQL_DB')
            )
        )
        if os.environ.get('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query and return all instances or a specific class's instances"""
        objects = {}
        if cls is None:
            for class_name, model in CLASSES.items():
                items = self.__session.query(model).all()
                for item in items:
                    key = "{}.{}".format(class_name, item.id)
                    objects[key] = item
        else:
            items = self.__session.query(cls).all()
            for item in items:
                key = "{}.{}".format(cls.__name__, item.id)
                objects[key] = item
        return objects

    def new(self, obj):
        """Add an object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes in the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete an object from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create tables in the database and set up a new session"""
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(bind=self.__engine, expire_on_commit=False))
        self.__session = Session()

    def close(self):
        """Remove the current session"""
        self.__session.remove()

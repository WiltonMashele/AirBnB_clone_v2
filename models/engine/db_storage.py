#!/usr/bin/python3
from sqlalchemy import (create_engine)
import os


user = os.environ.get('HBNB_MYSQL_USER')
pwd = os.environ.get('HBNB_MYSQL_PWD')
host = os.environ.get('HBNB_MYSQL_HOST')
database = os.environ.get('HBNB_MYSQL_DB')
env = os.environ.get('HBNB_ENV')


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            user, pwd, host, database), pool_pre_ping=True)
        if env == 'test':
            self.__engine.execute(f"DROP TABLE {database}.*")

    def all(self, cls=None):
        if cls is None:
            cls = [User, State, City, Amenity, Place, Review]
        query = self.__session.query(*cls).all()
        cls_objs = {}
        for obj in query:
            cls_objs[obj.name + '.' + obj.id] = obj
        return cls_objs

    def new(self, obj):
        self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def delete(self, obj=None):
        if obj:
            self.__session.delete(obj)

    def reload(self):
        from models.user import User
        from models.place import Place
        from models.state import State, Base as BaseState
        from models.city import City, Base as BaseCity
        from models.amenity import Amenity
        from models.review import Review
        BaseState.metadata.create_all(self.__engine)
        BaseCity.metadata.create_all(self.__engine)

        Session = scoped_session(sessionmaker(
            bind=engine, expire_on_commit=False))
        session = Session()

#!/usr/bin/python3
from sqlalchemy import (create_engine)
from sqlalchemy.orm import scoped_session, sessionmaker
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
        self.__engine = create_engine(
                'mysql+mysqldb://{}:{}@{}/{}'.format(
                    user, pwd, host, database), pool_pre_ping=True)
        if env == 'test':
            self.__engine.execute(f"DROP TABLE {database}.*")

    def all(self, cls=None):
        from models.user import User
        from models.place import Place
        from models.state import State, Base
        from models.city import City, Base
        from models.amenity import Amenity
        from models.review import Review

        if cls is None:
            cls = [State, City]
            query = []
            for c in cls:
                query += self.__session.query(c).all()
        else:
            query = self.__session.query(cls).all()
        cls_objs = {}
        for obj in query:
            cls_objs[obj.to_dict()['__class__'] + '.' + obj.id] = obj
        return cls_objs

    def new(self, obj):
        print('here')
        self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def delete(self, obj=None):
        if obj:
            self.__session.delete(obj)

    def reload(self):
        from models.user import User
        from models.place import Place
        from models.state import State, Base
        from models.city import City, Base
        from models.amenity import Amenity
        from models.review import Review
        Base.metadata.create_all(self.__engine)

        Session = scoped_session(
                sessionmaker(bind=self.__engine, expire_on_commit=False))
        self.__session = Session()

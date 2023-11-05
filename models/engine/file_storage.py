#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

CLASSES = {
    "Amenity": Amenity,
    "BaseModel": BaseModel,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User
}

class FileStorage:
    """Serializes instances to a JSON file and deserializes back to instances"""

    def __init__(self):
        # Path to the JSON file
        self.__file_path = "file.json"
        # Dictionary to store all objects by <class name>.id
        self.__objects = {}

    def all(self, cls=None):
        """Returns the dictionary __objects"""
        if cls is None:
            return self.__objects
        return {k: v for k, v in self.__objects.items() if isinstance(v, cls)}

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id"""
        if obj:
            key = f"{obj.__class__.____name__}.{obj.id}"
            self.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)"""
        json_objects = {k: v.to_dict() for k, v in self.__objects.items()}
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def delete(self, obj=None):
        """Deletes obj from __objects if it's inside"""
        if obj:
            key = f"{obj.__class__.____name__}.{obj.id}"
            self.__objects.pop(key, None)

    def reload(self):
        """Deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as f:
                json_objects = json.load(f)
            for key, obj_dict in json_objects.items():
                class_name = obj_dict["__class__"]
                obj = CLASSES[class_name](**obj_dict)
                key = f"{class_name}.{obj.id}"
                self.__objects[key] = obj
        except FileNotFoundError:
            pass

    def close(self):
        """Closes the current session"""
        self.reload()

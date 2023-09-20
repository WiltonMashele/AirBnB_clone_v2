#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.amenity import Amenity

import os
env_value = os.environ.get('HBNB_TYPE_STORAGE')

class test_Amenity(test_basemodel):
    """ """
    if env_value != 'db':
        def __init__(self, *args, **kwargs):
            """ """
            super().__init__(*args, **kwargs)
            self.name = "Amenity"
            self.value = Amenity

        def test_name2(self):
            """ """
            new = self.value()
            self.assertEqual(type(new.name), str)

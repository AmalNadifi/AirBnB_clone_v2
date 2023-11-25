#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls is not None:
            # If cls is provided as a string, convert it to a class object
            if type(cls) == str:
                cls = eval(cls)
            my_dict = {}
            # Iterate through the items in the __objects dictionary
            for key, value in self.__objects.items():
                # Check if the type of the value
                # matches the provided class (cls)
                if type(value) == cls:
                    # If it matches, add it to the my_dict dictionary
                    my_dict[key] = value
                    # Return the filtered dictionary
                    # containing instances of the provided class
            return my_dict
        return self.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        class_name = obj.to_dict().get('__class__')
        obj_id = obj.to_dict().get('id')

        if class_name is None:
            print(f"Error: '__class__' is None for object {obj}")
            return

        if obj_id is None:
            print(f"Error: 'id' is None for object {obj}")
            return

        key = f"{class_name}.{obj_id}"
        self.all().update({key: obj})
       # self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """It Deletes the object from __objects"""
        if obj is not None:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """Deserializing
        the JSON file to objects
        """
        self.reload()

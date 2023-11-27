#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""

from models.base_model import BaseModel, Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy import (create_engine)
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from os import getenv
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage

env = getenv('HBNB_TYPE_STORAGE')
if env == 'db':
    storage = DBStorage()
else:
    storage = FileStorage()
storage.reload()

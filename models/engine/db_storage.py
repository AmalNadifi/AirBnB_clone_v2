#!/usr/bin/python3
"""This module is a database storage definition"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from models.base_model import BaseModel, Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from os import getenv

name2class = {'Amenity': Amenity, 'City': City, 'Place': Place,
              'State': State,
              'Review': Review,
              'User': User
              }


class DBStorage:
    """This is the DBStorage class

    Attributes:
        __engine
        __session
    """
    # Private class attributes
    __engine = None
    __session = None

    def __init__(self):
        """
        This method creates the engine with configuration
        from environment variables
        """
        # Setting the connection details for the database
        # from environment variables
        db_user = getenv("HBNB_MYSQL_USER")
        db_password = getenv("HBNB_MYSQL_PWD")
        db_host = getenv("HBNB_MYSQL_HOST")
        db_name = getenv("HBNB_MYSQL_DB")

        # Creating the engine with the specified dialect, driver,
        # and connection details
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(db_user, db_password, db_host,
                                             db_name), pool_pre_ping=True)

        # Dropping all tables if HBNB_ENV is 'test'
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ This method is to query all the objects in the database session"""

        # Check if the database session is available, and reload if not
        if not self.__session:
            self.reload()

        # Initialize an empty dictionary to store the queried objects
        results_dict = {}

        # If cls is a string, convert it to a class reference
        if type(cls) == str:
            cls = name2class.get(cls, None)

        # If cls is provided and not None, query objects of that class
        if cls:
            for obj in self.__session.query(cls):
                # Create a dictionary key using the class name and object ID
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                results_dict[key] = obj
        else:
            # If cls is not provided , list of classes to query
            classes_to_query = [State, City, User, Place, Review, Amenity]

            # Iterate through each class and query objects of each class
            for cls_to_query in classes_to_query:
                for obj in self.__session.query(cls_to_query):
                    # Create a dictionary key using the class name & object ID
                    key = "{}.{}".format(obj.__class__.__name__, obj.id)
                    results_dict[key] = obj

        # Return the dictionary of objects
        return results_dict

    def new(self, obj):
        """
        This method adds the object to the current database session"""
        if obj:
            self.__session.add(obj)

    def save(self):
        """
        This method commits all the changes in the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """
        This method deletes the object from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        This method creates tables and a new database session
        """
        try:
            # Clear the existing session, if any
            if self.__session:
                self.__session.close()

            # Create tables
            Base.metadata.create_all(self.__engine)

            # Use existing scoped session class &assign a new session to it
            self.__session = scoped_session(
                    sessionmaker(bind=self.__engine, expire_on_commit=False))
        except Exception as e:
            print(f"Error during reload: {e}")
            raise  # Reraise the exception to see the full traceback

    def get(self, cls, id):
        """
        This method is retrieving an object based on class name and id
        """
        if cls and id:
            objects = self.all(cls)
            key = "{}.{}".format(cls.__name__, id)
            return objects.get(key)
        return None

    def count(self, cls=None):
        """
        This method counts the number of objects in
        the database for a given class

        If cls is None, count all objects.
        """
        return len(self.all(cls))

    def close(self):
        """
        This method closes the current session
        """
        self.__session.close()

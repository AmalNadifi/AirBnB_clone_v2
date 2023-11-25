#!/usr/bin/python3
"""ThIs module defines a base class for all models in our hbnb clone"""
from sqlalchemy.ext.declarative import declarative_base
import models
from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String

# Creating a declarative base for SQLAlchemy
Base = declarative_base()


class BaseModel:
    """This class is a base class for all the hbnb models"""

    # Unique ID for the model, 60 characters, primary key, cannot be null
    id = Column(String(60), primary_key=True, nullable=False, unique=True)

    # Timestamp for when the instance was created, cannot be null
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    # Timestamp for when the instance was last updated, cannot be null
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """ This method instantiates a new model"""
        if not kwargs:
            # Generating a unique ID
            self.id = str(uuid4())
            # Setting the 'created_at','updated_at' timestamps to current time
            self.created_at = self.updated_at = datetime.now()
        else:
            for key, value in kwargs.items():
                if key == 'created_at':
                    # Converting the 'created_at' timestamp to a datetime obj
                    value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
                if key == 'updated_at':
                    # Converting the 'updated_at' timestamp to a datetime obj
                    value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
                if key != "__class__":
                    # Setting the attributes based on key-value pairs in kwargs
                    setattr(self, key, value)

            # If 'created_at' or 'updated_at' is not present in kwargs,
            # Set them to current time
            if 'created_at' not in kwargs:
                self.created_at = datetime.now()
            if 'updated_at' not in kwargs:
                self.updated_at = datetime.now()

    def __str__(self):
        """This method returns a string representation of the instance"""
        # Getting the class name as a string
        d = self.__dict__.copy()
        # Remove SQLAlchemys internal state attribute
        d.pop('_sa_instance_state', None)
        # Returning the formatted string representation of the instance
        return "[{}] ({}) {}".format(type(self).__name__, self.id, d)

    def save(self):
        """This method updates 'updated_at' with the current time
        and saves the instance
        """
        from models import storage
        # Updating the 'updated_at' timestamp to the current time
        self.updated_at = datetime.now()
        # Updating the 'id' if it's None
        if not self.id:
            self.id = str(uuid4())
        # Adding the new instance to the storage
        storage.new(self)
        # Saving the instance using the storage
        storage.save()

    def to_dict(self):
        """This method converts the instance into a dictionary format"""
        d = self.__dict__.copy()
        # Add the class name to the dictionary
        d["__class__"] = str(type(self).__name__)
        # Formatting the 'created_at''updated_at' timestamps as ISO strings

        d['created_at'] = self.created_at.isoformat()
        d['updated_at'] = self.updated_at.isoformat()
        # Removing SQLAlchemy internal state attribute
        d.pop('_sa_instance_state', None)
        # Returning a dictionary representation of the instance
        return d

    def delete(self):
        """This method deletes the current instance from storage"""
        from models.__init__ import storage
        # Deleting the instance from the storage
        models.storage.delete(self)

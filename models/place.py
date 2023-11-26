#!/usr/bin/python3
""" This is the Place Module for HBNB project """
from os import getenv
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Table, String, Integer, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


# Defining the association table for the many-to-many relationship
# between Place and Amenity
place_amenity = Table("place_amenity", Base.metadata,
                      Column("place_id", String(60),
                             ForeignKey("places.id"),
                             primary_key=True,
                             nullable=False),
                      Column("amenity_id", String(60),
                             ForeignKey("amenities.id"),
                             primary_key=True,
                             nullable=False))


class Place(BaseModel, Base):
    """
    This is the Place class

    Attributes:
        city_id: The city id
        user_id: The user id
        name: The name input
        description: The description string
        number_rooms(int) : The number of room
        number_bathrooms(int): The number of bathrooms
        max_guest(int): The maximum number of guests
        price_by_night(int): The price for a staying
        latitude(float): The latitude
        longitude(float): The longitude
        amenity_ids(list): The list of Amenity ids
    """
    __tablename__ = "places"

    if getenv("HBNB_TYPE_STORAGE") == "db":
        city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024))
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float)
        longitude = Column(Float)
        amenity_ids = []

        # Relationship with Review and Amenity for database storage
        reviews = relationship("Review", cascade='all, delete',
                               backref="place")

        amenities = relationship("Amenity", secondary=place_amenity,
                                 viewonly=False,
                                 back_populates="place_amenities")
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """
            This method returns a list of reviews.id for non-database storage
            """
            # Getting all the objects from non-database storage
            all_objects = models.storage.all()
            reviews_list = []
            result = []

            # Filtering and appending reviews to the list
            for key in all_objects:
                # Replacing the dot with a space
                # and splitting the key into parts
                obj_parts = key.replace('.', ' ').split()
                if obj_parts[0] == 'Review':
                    reviews_list.append(all_objects[key])

            # Filtering the reviews based on place_id and appending to result
            for review in reviews_list:
                if review.place_id == self.id:
                    result.append(review)
            return result

        @property
        def amenities(self):
            """
            This method returns a list of amenity ids for non-database storage
            """
            return self.amenity_ids

        @amenities.setter
        def amenities(self, obj=None):
            """
            This setter method appends amenity ids to the attribute
            for non-database storage
            """
            if isinstance(obj, Amenity) and obj.id not in self.amenity_ids:
                self.amenity_ids.append(obj.id)

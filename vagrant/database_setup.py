#!/usr/bin/env python

import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Restaurant(Base):

	__tablename__ = "restaurant"
	restaurant_id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)

	@property
	def serialize(self):
		return dict(restaurant_id=self.restaurant_id, 
			        name=self.name)

class MenuItem(Base):

	__tablename__ = "menu_item"
	name = Column(String(80), nullable=False)
	menu_id = Column(Integer, primary_key=True)
	description = Column(String(250))
	price = Column(String(8))
	course = Column(String(250))
	restaurant_id = Column(Integer, ForeignKey("restaurant.restaurant_id"))
	restaurant = relationship(Restaurant)

	@property
	def serialize(self):
		return dict(name=self.name, 
			        description=self.description, 
			        menu_id=self.menu_id, 
			        price=self.price, 
			        course=self.course)

engine = create_engine("sqlite:///restaurantmenu.db")

Base.metadata.create_all(engine)
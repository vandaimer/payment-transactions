from sqlalchemy import Column, Integer, String, ForeignKey

from db import BaseSQLAlchemy


class Restaurant(BaseSQLAlchemy):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    cnpj = Column(String, nullable=False)
    owner = Column(String, nullable=False)
    phone = Column(String, nullable=False)


class Order(BaseSQLAlchemy):
    id = Column(Integer, primary_key=True)
    client = Column(String, nullable=False)
    price = Column(String, nullable=False)
    description = Column(String, nullable=False)
    restaurant = Column(Integer, ForeignKey('restaurant.id'))

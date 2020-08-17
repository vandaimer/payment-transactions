from sqlalchemy import Column, Integer, String, ForeignKey

from db import BaseSQLAlchemy


class Restaurant(BaseSQLAlchemy):
    __tablename__ = 'Restaurant'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    cnpj = Column(String)
    owner = Column(String)
    phone = Column(String)


class Order(BaseSQLAlchemy):
    __tablename__ = 'Order'

    id = Column(Integer, primary_key=True)
    client = Column(String)
    price = Column(String)
    description = Column(String)
    restaurant = Column(Integer, ForeignKey('Restaurant.id'))

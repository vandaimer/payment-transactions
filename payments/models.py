from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import validates

from db import BaseSQLAlchemy


class Restaurant(BaseSQLAlchemy):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    cnpj = Column(String, nullable=False)
    owner = Column(String, nullable=False)
    phone = Column(String, nullable=False)

    @validates('name', 'cpnj', 'owner', 'phone')
    def validate_empty_fields(self, key, value):
        if value == '' or value.strip() == '':
            raise ValueError(f"Field {key} must be not empty.")
        return value


class Transaction(BaseSQLAlchemy):
    id = Column(Integer, primary_key=True)
    client = Column(String, nullable=False)
    price = Column(String, nullable=False)
    description = Column(String, nullable=False)
    restaurant = Column(Integer, ForeignKey('restaurant.id'))

from .models import Restaurant, Transaction
from pydantic_sqlalchemy import sqlalchemy_to_pydantic


RestaurantSchema = sqlalchemy_to_pydantic(Restaurant, exclude={"id"})

TransactionSchema = sqlalchemy_to_pydantic(Transaction, exclude={"id"})

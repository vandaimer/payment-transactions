from .models import Restaurant, Order
from pydantic_sqlalchemy import sqlalchemy_to_pydantic


RestaurantSchema = sqlalchemy_to_pydantic(Restaurant, exclude={"id"})

OrderSchema = sqlalchemy_to_pydantic(Order, exclude={"id"})

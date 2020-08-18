from typing import List
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from pydantic import BaseModel

from .models import Restaurant, Transaction


RestaurantSchema = sqlalchemy_to_pydantic(Restaurant, exclude={"id"})

TransactionSchema = sqlalchemy_to_pydantic(Transaction, exclude={"id"})

class ListOfTransactionSchema(BaseModel):
    estabelecimento: RestaurantSchema = None
    recebimentos: List[TransactionSchema] = []

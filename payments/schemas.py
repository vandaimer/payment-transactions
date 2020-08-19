from typing import List

from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from pydantic import BaseModel

from .models import Restaurant, Transaction


RestaurantSchema = sqlalchemy_to_pydantic(Restaurant, exclude={"id"})

TransactionSchema = sqlalchemy_to_pydantic(Transaction, exclude={"id"})

class RestaurantResponseSchema(BaseModel):
    nome: str
    cnpj: str
    dono: str
    telefone: str

class TransactionResponseSchema(BaseModel):
    cliente: str
    valor: float
    descricao: str

class ListOfTransactionSchema(BaseModel):
    estabelecimento: RestaurantResponseSchema = None
    recebimentos: List[TransactionResponseSchema] = []
    total_recebido: float

class NewTransactionSchema(BaseModel):
    estabelecimento: str
    cliente: str
    valor: float
    descricao: str


class ReturnNewTransactionSchema(BaseModel):
    aceito: bool

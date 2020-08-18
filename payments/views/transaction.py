import re

from payments.models import Transaction as TransactionModel
from payments.models import Restaurant as RestaurantModel
from payments.schemas import ListOfTransactionSchema, ReturnNewTransactionSchema


class Transaction:
    CNPJ_REGEX = '^(\d{2})\.?(\d{3})\.?(\d{3})\/?(\d{4})\-?(\d{2})$'

    @staticmethod
    def all(cnpj, db):
        restaurant = db.query(RestaurantModel).filter(RestaurantModel.cnpj == str(cnpj)).one()
        transactions = db.query(TransactionModel).filter(TransactionModel.restaurant == restaurant.id).all()
        return ListOfTransactionSchema(estabelecimento=restaurant, recebimentos=transactions)

    @staticmethod
    def create(transaction, db):
        restaurant = db.query(RestaurantModel).filter(RestaurantModel.cnpj == str(transaction.estabelecimento)).one()

        new_transaction = TransactionModel(client=transaction.cliente, price=transaction.valor, description=transaction.descricao, restaurant=restaurant.id)

        db.add(new_transaction)
        db.commit()

        return ReturnNewTransactionSchema(aceito=True)

    @staticmethod
    def is_valid_cnpj(cnpj):
        return re.search(Transaction.CNPJ_REGEX, cnpj)

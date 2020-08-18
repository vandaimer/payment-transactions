import re

from payments.models import Transaction as TransactionModel
from payments.models import Restaurant as RestaurantModel
from payments.schemas import ListOfTransactionSchema, ReturnNewTransactionSchema


class Transaction:
    CNPJ_REGEX = '^(\d{2})\.?(\d{3})\.?(\d{3})\/?(\d{4})\-?(\d{2})$'
    CPF_REGEX = '^(\d{3})\.?(\d{3})\.?(\d{3})\-?(\d{2})$'

    @staticmethod
    def all(cnpj, db):
        restaurant = db.query(RestaurantModel).filter(RestaurantModel.cnpj == str(cnpj)).one()
        transactions = db.query(TransactionModel).filter(TransactionModel.restaurant == restaurant.id).all()
        return ListOfTransactionSchema(estabelecimento=restaurant, recebimentos=transactions)

    @staticmethod
    def create(transaction, db):
        transaction_validated = Transaction.validate_transaction(transaction)

        if transaction_validated is None:
            return ReturnNewTransactionSchema(aceito=False)

        restaurant = db.query(RestaurantModel).filter(RestaurantModel.cnpj == transaction_validated.get('estabelecimento')).one()

        new_transaction = TransactionModel(client=transaction_validated.get('cliente'), price=transaction_validated.get('valor'), description=transaction_validated.get('descricao'), restaurant=restaurant.id)

        db.add(new_transaction)
        db.commit()

        return ReturnNewTransactionSchema(aceito=True)

    @staticmethod
    def validate_transaction(transaction):
        cnpj = Transaction.is_valid_cnpj(transaction.estabelecimento)

        if cnpj is None:
            return None

        cnpj = ''.join(cnpj.groups())

        cpf = Transaction.is_valid_cpf(transaction.cliente)

        if cpf is None:
            return None

        cpf = ''.join(cpf.groups())

        if transaction.valor <= 0:
            return None

        return {**transaction.dict(), 'estabelecimento': cnpj, 'cliente': cpf}


    @staticmethod
    def is_valid_cnpj(cnpj):
        return re.search(Transaction.CNPJ_REGEX, cnpj)

    @staticmethod
    def is_valid_cpf(cpf):
        return re.search(Transaction.CPF_REGEX, cpf)

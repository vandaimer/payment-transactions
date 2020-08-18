from payments.models import Transaction as TransactionModel
from payments.models import Restaurant as RestaurantModel
from payments.schemas import ListOfTransactionSchema, ReturnNewTransactionSchema


class Transaction:

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

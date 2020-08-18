from payments.models import Transaction as TransactionModel
from payments.models import Restaurant as RestaurantModel
from payments.schemas import ListOfTransactionSchema


class Transaction:

    @staticmethod
    def all(cnpj, db):
        restaurant = db.query(RestaurantModel).filter(RestaurantModel.cnpj == str(cnpj)).one()
        transactions = db.query(TransactionModel).filter(TransactionModel.restaurant == restaurant.id).all()
        return ListOfTransactionSchema(estabelecimento=restaurant, recebimentos=transactions)

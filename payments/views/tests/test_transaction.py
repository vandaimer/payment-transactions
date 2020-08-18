import mock
from alchemy_mock.mocking import UnifiedAlchemyMagicMock

from payments.views import Transaction
from payments.models import Transaction as TransactionModel
from payments.models import Restaurant as RestaurantModel
from payments.schemas import TransactionSchema


class TestTransaction:
    def test_all(self, mocker):
        cnpj_mock = 'cnpj_mock'
        string_mock = 'string_mock'
        expected_restaurant = {
            'name': string_mock,
            'cnpj': string_mock,
            'owner': string_mock,
            'phone': string_mock,
        }
        restaurant_mock = RestaurantModel(**expected_restaurant)
        transaction_mock = TransactionModel(client=string_mock, price=1, description=string_mock, restaurant=1)

        session = UnifiedAlchemyMagicMock(data=[
            (
                [mock.call.query(RestaurantModel),
                 mock.call.filter(RestaurantModel.cnpj == cnpj_mock)],
                [restaurant_mock]
            ),
            (
                [mock.call.query(TransactionModel),
                 mock.call.filter(TransactionModel.restaurant == restaurant_mock.id)],
                [transaction_mock]
            ),
        ])

        response = Transaction.all(cnpj_mock, session)

        estabelecimento = dict(response.estabelecimento)

        assert estabelecimento == expected_restaurant
        assert len(response.recebimentos) == 1

import re
import mock
import pytest
from alchemy_mock.mocking import UnifiedAlchemyMagicMock, AlchemyMagicMock

from payments.views import Transaction
from payments.models import Transaction as TransactionModel
from payments.models import Restaurant as RestaurantModel
from payments.schemas import NewTransactionSchema


def mock_is_valid_cnpj(mocker, cnpj):
    mocker.patch(
        'payments.views.transaction.Transaction.is_valid_cnpj',
        side_effect=lambda x: re.search(
            f"({cnpj})",
            cnpj))

def mock_is_valid_cpf(mocker, cpf):
    mocker.patch(
        'payments.views.transaction.Transaction.is_valid_cpf',
        side_effect=lambda x: re.search(
            f"({cpf})",
            cpf))


class TestTransaction:
    def setup_method(self, method):
        self.cnpj_mock = 'cnpj_mock'
        self.cpf_mock = 'cpf_mock'
        self.string_mock = 'string_mock'
        self.transaction_mock = TransactionModel(
            client=self.string_mock,
            description=self.string_mock,
            restaurant=1)
        self.new_transaction = NewTransactionSchema(
            estabelecimento=self.cnpj_mock,
            cliente=self.cpf_mock,
            valor=1,
            descricao="",
            restaurant=1)

    def test_all(self, mocker):
        price = 1
        self.transaction_mock.price = price
        mocker.patch(
            'payments.views.transaction.Transaction.is_valid_cnpj',
            side_effect=lambda x: re.search(
                f"({self.cnpj_mock})",
                self.cnpj_mock))

        expected_restaurant = {
            'name': self.string_mock,
            'cnpj': self.string_mock,
            'owner': self.string_mock,
            'phone': self.string_mock,
        }

        restaurant_mock = RestaurantModel(**expected_restaurant)

        session = UnifiedAlchemyMagicMock(data=[
            (
                [mock.call.query(RestaurantModel),
                 mock.call.filter(RestaurantModel.cnpj == self.cnpj_mock)],
                [restaurant_mock]
            ),
            (
                [mock.call.query(TransactionModel),
                 mock.call.filter(
                     TransactionModel.restaurant == restaurant_mock.id)],
                [self.transaction_mock]
            ),
        ])

        response = Transaction.all(self.cnpj_mock, session)

        estabelecimento = dict(response.estabelecimento)

        assert estabelecimento == expected_restaurant
        assert len(response.recebimentos) == len([self.transaction_mock])
        assert response.total_recebido == price

    def test_all_invalid_cnpj(self, mocker):
        session = AlchemyMagicMock()

        with pytest.raises(ValueError, match="Invalid CNPJ."):
            Transaction.all(self.cnpj_mock, session)

    def test_invalid_cpnj_method(self, mocker):
        invalid_cnpj = Transaction.is_valid_cnpj(self.cnpj_mock)

        assert invalid_cnpj is None

        mock_is_valid_cnpj(mocker, self.cnpj_mock)

        valid_cnpj = Transaction.is_valid_cnpj(self.cnpj_mock)

        assert valid_cnpj is not None

    def test_invalid_cpf_method(self, mocker):
        invalid_cpf = Transaction.is_valid_cpf(self.cpf_mock)

        assert invalid_cpf is None

        mock_is_valid_cpf(mocker, self.cpf_mock)

        valid_cpf = Transaction.is_valid_cpf(self.cpf_mock)

        assert valid_cpf is not None

    def test_validate_transaction(self, mocker):
        price = 1
        mock_is_valid_cnpj(mocker, self.cnpj_mock)
        mock_is_valid_cpf(mocker, self.cpf_mock)

        expected = {
            **self.new_transaction.dict(),
            'estabelecimento': self.cnpj_mock,
            'cliente': self.cpf_mock}

        response = Transaction.validate_transaction(self.new_transaction)

        assert response is not None
        assert response == expected

    def test_validate_transaction_invalid_cnpj(self, mocker):
        self.new_transaction.estabelecimento = 'InvalidCNPJ'
        response = Transaction.validate_transaction(self.new_transaction)

        assert response is None

    def test_validate_transaction_invalid_cpf(self, mocker):
        self.new_transaction.cliente = 'InvalidCPF'
        self.new_transaction.estabelecimento = '45283163000167'

        response = Transaction.validate_transaction(self.new_transaction)

        assert response is None

    def test_validate_transaction_invalid_price(self, mocker):
        mock_is_valid_cnpj(mocker, self.cnpj_mock)
        mock_is_valid_cpf(mocker, self.cpf_mock)

        self.new_transaction.valor = 0

        response = Transaction.validate_transaction(self.new_transaction)

        assert response is None

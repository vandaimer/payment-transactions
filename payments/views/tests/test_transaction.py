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

        self.expected_restaurant = {
            'name': self.string_mock,
            'cnpj': self.string_mock,
            'owner': self.string_mock,
            'phone': self.string_mock,
        }

        self.restaurant_mock = RestaurantModel(**self.expected_restaurant)

    def test_all(self, mocker):
        price = 1
        self.transaction_mock.price = price
        mocker.patch(
            'payments.views.transaction.Transaction.is_valid_cnpj',
            side_effect=lambda x: re.search(
                f"({self.cnpj_mock})",
                self.cnpj_mock))

        session = UnifiedAlchemyMagicMock(data=[
            (
                [mock.call.query(RestaurantModel),
                 mock.call.filter(RestaurantModel.cnpj == self.cnpj_mock)],
                [self.restaurant_mock]
            ),
            (
                [mock.call.query(TransactionModel),
                 mock.call.filter(
                     TransactionModel.restaurant == self.restaurant_mock.id)],
                [self.transaction_mock]
            ),
        ])

        response = Transaction.all(self.cnpj_mock, session)

        estabelecimento = dict(response.estabelecimento)

        assert estabelecimento['cnpj'] == self.expected_restaurant['cnpj']
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

    def test_create(self, mocker):
        restaurant_id = 1
        self.restaurant_mock.id = restaurant_id

        mocker.patch(
            'payments.views.transaction.Transaction.validate_transaction',
            side_effect=lambda x: self.new_transaction.dict())

        session = UnifiedAlchemyMagicMock(data=[
            (
                [mock.call.query(RestaurantModel),
                 mock.call.filter(RestaurantModel.cnpj == self.cnpj_mock)],
                [self.restaurant_mock]
            ),
        ])

        transaction = TransactionModel(
            client=self.new_transaction.cliente,
            price=self.new_transaction.valor,
            description=self.new_transaction.descricao,
            restaurant=restaurant_id,
        )

        session.add(transaction)

        Transaction.create(self.new_transaction, session)

        session.query.return_value.filter.\
            assert_called_once_with(RestaurantModel.cnpj == self.cnpj_mock)
        session.commit.assert_called_once()

    def test_create_on_failure(self, mocker):
        restaurant_id = 1
        self.restaurant_mock.id = restaurant_id

        mocker.patch(
            'payments.views.transaction.Transaction.validate_transaction',
            side_effect=lambda x: None)

        session = AlchemyMagicMock()

        response = Transaction.create(self.new_transaction, session)

        assert response.aceito is False

    def test_build_responde(self, mocker):
        self.transaction_mock.price = 1
        response = Transaction.build_response(self.transaction_mock)

        expected = {
            'cliente': self.transaction_mock.client,
            'valor': self.transaction_mock.price,
            'descricao': self.transaction_mock.description,
        }

        assert response.dict() == expected

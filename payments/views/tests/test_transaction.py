import re
import mock
import pytest
from alchemy_mock.mocking import UnifiedAlchemyMagicMock, AlchemyMagicMock

from payments.views import Transaction
from payments.models import Transaction as TransactionModel
from payments.models import Restaurant as RestaurantModel
from payments.schemas import NewTransactionSchema


class TestTransaction:
    def test_all(self, mocker):
        cnpj_mock = 'cnpj_mock'
        string_mock = 'string_mock'
        price = 1
        mocker.patch(
            'payments.views.transaction.Transaction.is_valid_cnpj',
            side_effect=lambda x: re.search(
                f"({cnpj_mock})",
                cnpj_mock))

        expected_restaurant = {
            'name': string_mock,
            'cnpj': string_mock,
            'owner': string_mock,
            'phone': string_mock,
        }

        restaurant_mock = RestaurantModel(**expected_restaurant)
        transaction_mock = TransactionModel(
            client=string_mock,
            price=price,
            description=string_mock,
            restaurant=1)

        session = UnifiedAlchemyMagicMock(data=[
            (
                [mock.call.query(RestaurantModel),
                 mock.call.filter(RestaurantModel.cnpj == cnpj_mock)],
                [restaurant_mock]
            ),
            (
                [mock.call.query(TransactionModel),
                 mock.call.filter(
                     TransactionModel.restaurant == restaurant_mock.id)],
                [transaction_mock]
            ),
        ])

        response = Transaction.all(cnpj_mock, session)

        estabelecimento = dict(response.estabelecimento)

        assert estabelecimento == expected_restaurant
        assert len(response.recebimentos) == len([transaction_mock])
        assert response.total_recebido == price

    def test_all_invalid_cnpj(self, mocker):
        session = AlchemyMagicMock()
        cnpj_mock = 'cnpj_mock'

        with pytest.raises(ValueError, match="Invalid CNPJ."):
            Transaction.all(cnpj_mock, session)

    def test_invalid_cpnj_method(self, mocker):
        cnpj_mock = 'cnpj_mock'

        invalid_cnpj = Transaction.is_valid_cnpj(cnpj_mock)

        assert invalid_cnpj is None

        mocker.patch(
            'payments.views.transaction.Transaction.is_valid_cnpj',
            side_effect=lambda x: re.search(
                f"({cnpj_mock})",
                cnpj_mock))

        valid_cnpj = Transaction.is_valid_cnpj(cnpj_mock)

        assert valid_cnpj is not None

    def test_invalid_cpf_method(self, mocker):
        cpf_mock = 'cpf_mock'

        invalid_cpf = Transaction.is_valid_cpf(cpf_mock)

        assert invalid_cpf is None

        mocker.patch(
            'payments.views.transaction.Transaction.is_valid_cpf',
            side_effect=lambda x: re.search(
                f"({cpf_mock})",
                cpf_mock))

        valid_cpf = Transaction.is_valid_cpf(cpf_mock)

        assert valid_cpf is not None

    def test_validate_transaction(self, mocker):
        mock_document = 'mock_document'
        valor = 1
        mocker.patch(
            'payments.views.transaction.Transaction.is_valid_cnpj',
            side_effect=lambda x: re.search(
                f"({mock_document})",
                mock_document))
        mocker.patch(
            'payments.views.transaction.Transaction.is_valid_cpf',
            side_effect=lambda x: re.search(
                f"({mock_document})",
                mock_document))

        transaction_mock = NewTransactionSchema(
            estabelecimento=mock_document,
            cliente=mock_document,
            valor=valor,
            descricao="",
            restaurant=1)

        expected = {
            **transaction_mock.dict(),
            'estabelecimento': mock_document,
            'cliente': mock_document}

        response = Transaction.validate_transaction(transaction_mock)

        assert response == expected

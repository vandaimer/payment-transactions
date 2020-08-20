import mock
from alchemy_mock.mocking import UnifiedAlchemyMagicMock

from payments.views import Restaurant
from payments.models import Restaurant as RestaurantModel
from payments.schemas import RestaurantSchema


class TestRestaurant:
    def setup_method(self, method):
        self.string_mock = 'string_mock'

    def test_create(self, mocker):
        expected_restaurant = {
            'name': self.string_mock,
            'cnpj': self.string_mock,
            'owner': self.string_mock,
            'phone': self.string_mock,
        }
        session = UnifiedAlchemyMagicMock(data=[
            (
                [mock.call.add(RestaurantModel)]
            )
        ])

        restaurant_mock = RestaurantSchema(**expected_restaurant)

        response = Restaurant.create(restaurant_mock, session)

        session.commit.assert_called_once()

        assert response.nome == expected_restaurant['name']
        assert response.cnpj == expected_restaurant['cnpj']
        assert response.dono == expected_restaurant['owner']
        assert response.telefone == expected_restaurant['phone']

    def test_build_responde(self, mocker):
        restaurant = RestaurantModel(
            name=self.string_mock,
            cnpj=self.string_mock,
            owner=self.string_mock,
            phone=self.string_mock
        )

        response = Restaurant.build_response(restaurant)

        expected = {
            'nome': self.string_mock,
            'cnpj': self.string_mock,
            'dono': self.string_mock,
            'telefone': self.string_mock,
        }

        assert response.dict() == expected

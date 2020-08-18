import mock
from alchemy_mock.mocking import UnifiedAlchemyMagicMock

from payments.views import Restaurant
from payments.models import Restaurant as RestaurantModel
from payments.schemas import RestaurantSchema


class TestRestaurant:
    def test_create(self, mocker):
        string_mock = 'string_mock'
        expected_restaurant = {
            'name': string_mock,
            'cnpj': string_mock,
            'owner': string_mock,
            'phone': string_mock,
        }
        session = UnifiedAlchemyMagicMock(data=[
            (
                [mock.call.add(RestaurantModel)]
            )
        ])

        restaurant_mock = RestaurantSchema(**expected_restaurant)

        response = Restaurant.create(restaurant_mock, session)

        session.commit.assert_called_once()

        assert response.name == expected_restaurant['name']
        assert response.cnpj == expected_restaurant['cnpj']
        assert response.owner == expected_restaurant['owner']
        assert response.phone == expected_restaurant['phone']

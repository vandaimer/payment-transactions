from payments.models import Restaurant as RestaurantModel
from payments.schemas import RestaurantResponseSchema


class Restaurant:

    @staticmethod
    def create(restaurant, db):
        new_restaurant = RestaurantModel(**restaurant.dict())
        db.add(new_restaurant)
        db.commit()

        return Restaurant.build_response(new_restaurant)

    @staticmethod
    def build_response(restaurant):
        return RestaurantResponseSchema(
            nome=restaurant.name,
            cnpj=restaurant.cnpj,
            dono=restaurant.owner,
            telefone=restaurant.phone,
        )

from payments.models import Restaurant as RestaurantModel


class Restaurant:

    @staticmethod
    def create(restaurant, db):
        new_restaurant = RestaurantModel(**restaurant.dict())
        db.add(new_restaurant)
        db.commit()

        return new_restaurant

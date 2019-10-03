
from briw.classes.drink import Drink
from briw.data import texts


class Person:

    def __init__(self, name=None, favourite_drink: Drink = None, person_id=None):
        self.person_id = person_id
        self.name = name
        self.favourite_drink = favourite_drink

    def set_favourite_drink(self, new_favourite_drink):
        self.favourite_drink = new_favourite_drink

    def to_json(self):
        drink_to_show = texts.NOT_FAVOURITE_DRINK
        if self.favourite_drink != None:
            drink_to_show = self.favourite_drink.to_json()
        return {
            'Id': self.person_id,
            'Name': self.name,
            'Favourite Drink': drink_to_show
        }

    def to_no_drink_json(self):
        return {
            'Id': self.person_id,
            'Name': self.name,
        }


from briw.classes.drink import Drink


class Person:

    def __init__(self, name=None, favourite_drink: Drink = None, person_id=None):
        self.person_id = person_id
        self.name = name
        self.favourite_drink = favourite_drink

    def set_favourite_drink(self, new_favourite_drink):
        self.favourite_drink = new_favourite_drink

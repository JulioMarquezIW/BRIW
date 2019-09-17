
from briw.classes.drink import Drink


class Person:

    def __init__(self, name, favourite_drink: Drink = None):
        self.name = name
        self.favourite_drink = favourite_drink

    def set_favourite_drink(self, new_favourite_drink):
        self.favourite_drink = new_favourite_drink

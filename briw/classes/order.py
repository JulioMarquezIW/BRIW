

from briw.classes.person import Person
from briw.classes.drink import Drink


class Order:

    def __init__(self, person: Person, drink: Drink):
        self.person = person
        self.drink = drink

    def print_order(self):
        print(f"{self.person.name} want {self.drink.name}")



from briw.classes.person import Person
from briw.classes.drink import Drink


class Order:

    def __init__(self, person: Person, drink: Drink, order_id=None):
        self.person = person
        self.drink = drink
        self.order_id = order_id

    def print_order(self):
        print(f"{self.person.name} want {self.drink.name}")

    def to_json(self):
        return {
            'Id': self.order_id,
            'Person': self.person.to_no_drink_json(),
            'Drink': self.drink.to_json()
        }


from person import Person
from drink import Drink

from order import Order
import datetime


class Round:

    def __init__(self):
        self.orders = []
        self.date = datetime.datetime.now()

    def add_order(self, person: Person, drink: Drink):
        self.orders.append(Order(person, drink))

    def print_round(self):
        for order in self.orders:
            order.print_order()


# d1 = Drink('Water')
# d2 = Drink('Coffee')
# p1 = Person('Julio', d1)
# p2 = Person('Henry', d2)

# r = Round()

# r.add_order(p1, p1.favourite_drink)
# r.add_order(p2, p2.favourite_drink)

# r.print_round()

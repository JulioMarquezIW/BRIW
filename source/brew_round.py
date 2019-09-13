
from person import Person
from drink import Drink

from order import Order
import datetime


class Round:

    def __init__(self, date=datetime.datetime.now()):
        self.orders = []
        self.date = date

    def add_order(self, person: Person, drink: Drink):
        self.orders.append(Order(person, drink))

    def add_order_list(self, orders):
        self.orders += orders

    def print_round(self):
        for order in self.orders:
            order.print_order()

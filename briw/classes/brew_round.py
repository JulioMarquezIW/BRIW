
from briw.classes.person import Person
from briw.classes.drink import Drink
from briw.classes.order import Order
import datetime


class Round:

    def __init__(self, orders=[], date=datetime.datetime.now(), brewer: Person = None, isOpen=True):
        self.orders = orders
        self.date = date
        self.brewer = brewer
        self.isOpen = isOpen

    def add_order(self, person: Person, drink: Drink):
        self.orders.append(Order(person, drink))

    def add_order_list(self, orders):
        self.orders += orders

    def print_round(self):
        for order in self.orders:
            order.print_order()

    def close_round(self):
        self.isOpen = False

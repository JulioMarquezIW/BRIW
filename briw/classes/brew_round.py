
from briw.classes.person import Person
from briw.classes.drink import Drink
from briw.classes.order import Order
import datetime


class Round:

    def __init__(self, orders=[], open_date=datetime.datetime.now(),
                 brewer: Person = None, is_open=True, round_id=None):
        self.orders = orders
        self.open_date = open_date
        self.brewer = brewer
        self.is_open = is_open
        self.round_id = round_id

    def add_order(self, person: Person, drink: Drink):
        self.orders.append(Order(person, drink))

    def add_order_list(self, orders):
        self.orders += orders

    def print_round(self):
        for order in self.orders:
            order.print_order()

    def close_round(self):
        self.is_open = False


from briw.classes.person import Person
from briw.classes.drink import Drink
from briw.classes.order import Order
from briw.data import texts
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

    def get_string_date(self):
        return self.open_date.strftime(texts.DATE_FORMAT)

    def to_json(self):
        status = texts.CLOSE
        if self.is_open:
            status = texts.OPEN
        return {
            'Brewer': self.brewer.to_no_drink_json(),
            'Status': status,
            'Round ID': self.round_id,
            'Open date': self.get_string_date(),
            'Orders': [order.to_json() for order in self.orders]
        }

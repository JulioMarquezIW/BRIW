from json import JSONEncoder
from briw.classes.brew_round import Round
from briw.classes.order import Order
from briw.data import texts
import json


class RoundEncoder(JSONEncoder):

    def default(self, object):

        if isinstance(object, Round):
            status = texts.CLOSE
            if object.is_open:
                status = texts.OPEN

            orders = []
            for order in object.orders:
                orders.append({
                    'Person': order.person.name,
                    'Drink': order.drink.name
                })

            return {
                'open_date': object.open_date.strftime(texts.DATE_FORMAT),
                'brewer': object.brewer.name,
                'status': status,
                'orders': orders
            }

        else:
            # call base class implementation which takes care of
            # raising exceptions for unsupported types
            return json.JSONEncoder.default(self, object)

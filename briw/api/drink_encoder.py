from json import JSONEncoder
from briw.classes.drink import Drink
import json


class DrinkEncoder(JSONEncoder):

    def default(self, object):

        if isinstance(object, Drink):
            return {'name': object.name}

        else:
            # call base class implementation which takes care of
            # raising exceptions for unsupported types
            return json.JSONEncoder.default(self, object)

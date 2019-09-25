from json import JSONEncoder
from briw.classes.person import Person
import json


class PeopleEncoder(JSONEncoder):

    def default(self, object):

        if isinstance(object, Person):
            return {'name': object.name, 'favourite_drink': object.favourite_drink.name}

        else:
            # call base class implementation which takes care of
            # raising exceptions for unsupported types
            return json.JSONEncoder.default(self, object)

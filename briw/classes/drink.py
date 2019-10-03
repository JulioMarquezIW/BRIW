

class Drink:

    def __init__(self, name=None, drink_id=None):
        self.drink_id = drink_id
        self.name = name

    def to_json(self):
        return {
            'Id': self.drink_id,
            'Name': self.name
        }

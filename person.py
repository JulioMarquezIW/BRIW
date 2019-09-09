

class Person:

    def __init__(self, name, favourite_drink):
        self.name = name
        self.typical_drink = favourite_drink

    def set_favourite_drink(self, new_favourite_drink):
        self.typical_drink = new_favourite_drink

    def print_typical_drink(self):
        print(f"{self.name} love {self.typical_drink}")


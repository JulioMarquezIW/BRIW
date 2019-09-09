

from person import Person
from data import people, drinks
import random

group = []


def populate():
    # Auxiliary function populate the info randomly
    #
    # Returns a group of persons with randoms names and drinks
    for p in people:
        per = Person(p, drinks[random.randint(0, len(drinks) - 1)])
        group.append(per)
    return group

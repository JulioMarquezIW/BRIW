import unittest


# from briw.functions import functions
from briw.classes.person import Person
from briw.classes.drink import Drink
# from briw.functions import printer_aux

from briw.persistence.people_controller import get_people_from_database, save_new_user_in_database


class Test_Methods(unittest.TestCase):

    def test_get_people_from_database(self):
        people = get_people_from_database()
        self.assertTrue(len(people) != 0)


if __name__ == '__main__':
    unittest.main()

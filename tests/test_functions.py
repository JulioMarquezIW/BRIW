import unittest
from unittest.mock import patch


from briw.functions import functions
from briw.classes.person import Person
from briw.classes.drink import Drink
from briw.functions import printer_aux


def mock_inputs(input_values):
    output = []

    def mock_input(s):
        output.append(s)
        return input_values.pop(0)
    functions.input = mock_input
    functions.print = lambda s: output.append(s)
    printer_aux.print = lambda s: output.append(s)


class Test_Methods(unittest.TestCase):

    # def test_ask_boolean(self):
    #     # INPUTS
    #     #   'test': Value to test that only admits Y or
    #     #   'Y': right value to indicate True
    #     inputs = ['test', 'Y']
    #     mock_inputs(inputs)
    #     result = functions.ask_boolean("test")

    #     self.assertTrue(result)

    # def test_ask_number(self):
    #     # INPUTS
    #     #   Several wrong choices and finally the right one
    #     test_number = '3'
    #     inputs = ['test', 'Y', '99', test_number]
    #     mock_inputs(inputs)
    #     result = functions.ask_number("test", 1, 10)

    #     self.assertTrue(result == int(test_number))

    # def test_ask_list_of_numbers(self):
    #     # INPUTS
    #     #   Incorrect interleaved options, which will be ignored
    #     incorrect_test_numbers = '2,3,99,1,hola,4'
    #     expected_result = [2, 3, 1, 4]
    #     inputs = [incorrect_test_numbers]
    #     mock_inputs(inputs)
    #     result = functions.ask_list_of_numbers("test", 1, 10)

    #     self.assertTrue(result == expected_result)

    # def test_ask_unique_name(self):
    #     test_name = 'TestName'
    #     repeat_name = 'Repeat'
    #     people = [Person(repeat_name), Person('Dani')]
    #     inputs = [repeat_name, test_name]
    #     mock_inputs(inputs)
    #     new_name = functions.ask_unique_name(people, 'test')

    #     self.assertEqual(new_name, test_name)

    # def test_set_favourite_drink(self):

    #     # INPUTS
    #     #   '1': person id in the people list
    #     #   '2': drink id in the drinks list
    #     input_values = ['1', '2']
    #     mock_inputs(input_values)

    #     people = [Person('Julio'), Person('Dani')]
    #     drinks = [Drink('Water'), Drink('Coffee')]

    #     people = functions.set_favourite_drink(people, drinks)

    #     self.assertTrue(people[0].name == 'Julio')
    #     self.assertTrue(people[0].favourite_drink.name == drinks[1].name)
    #     self.assertTrue(people[1].favourite_drink == None)

    @patch('briw.persistence.people_controller.save_new_user_in_database')
    def test_create_new_person_with_drink(self, save_new_user_in_database):
        # Select the first option to create
        testName = ' TestName '
        drinkOption = '1'

        # INPUTS
        # Julio: Repeated name to verify that it is not allowed to repeat name in the list of persons
        # TestName: Unique name
        # 'Y': option to select that I want to add the favorite drink of the new period.
        # '99': Incorrect number for the moment of choosing a drink from the list.
        # drinkOption: Correct number for the moment of choosing a drink from the list
        input_values = ['Julio', testName, 'Y', '99', drinkOption]
        mock_inputs(input_values)

        people = [Person('Julio'), Person('Dani')]
        drinks = [Drink('Water'), Drink('Coffee')]

        save_new_user_in_database.return_value = Person(
            testName, drinkOption, 12)
        people = functions.create_new_person(people, drinks)

        self.assertTrue(len(people) == 3)
        self.assertTrue(people[-1].name == testName.strip())
        self.assertTrue(
            people[-1].favourite_drink.name == drinks[int(drinkOption)-1].name)

    # def test_create_new_person_without_drink(self):
    #     # Select the first option to create
    #     testName = ' TestName '

    #     # INPUTS
    #     # Julio: Repeated name to verify that it is not allowed to repeat name in the list of persons
    #     # TestName: Unique name
    #     # 'N': option to select that I don't want to add the favorite drink of the new period.
    #     # '99': Incorrect number for the moment of choosing a drink from the list.
    #     # drinkOption: Correct number for the moment of choosing a drink from the list
    #     input_values = ['Julio', 'TestName', 'N']
    #     mock_inputs(input_values)

    #     people = [Person('Julio'), Person('Dani')]
    #     drinks = [Drink('Water'), Drink('Coffee')]

    #     people = functions.create_new_person(people, drinks)

    #     self.assertTrue(len(people) == 3)
    #     self.assertTrue(people[len(people)-1].name == testName.strip())
    #     self.assertTrue(
    #         people[len(people)-1].favourite_drink == None)

    # def test_add_drink(self):
    #     new_drink_name = 'Beer'
    #     drinks = [Drink('Water'), Drink('Coffee')]
    #     input_values = ['Water', new_drink_name]
    #     mock_inputs(input_values)

    #     new_drinks = functions.add_drink(drinks)

    #     self.assertTrue(len(new_drinks) == 3)
    #     self.assertTrue(drinks[len(drinks)-1].name == new_drink_name)


if __name__ == '__main__':
    unittest.main()

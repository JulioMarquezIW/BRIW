import unittest
from unittest.mock import patch


from briw.functions import functions
from briw.classes.person import Person
from briw.classes.drink import Drink
from briw.classes.brew_round import Round
from briw.classes.order import Order
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

    def test_ask_boolean(self):
        # INPUTS
        #   'test': Value to test that only admits Y or
        #   'Y': right value to indicate True
        inputs = ['test', 'Y']
        mock_inputs(inputs)
        result = functions.ask_boolean("test")

        self.assertTrue(result)

    def test_ask_number(self):
        # INPUTS
        #   Several wrong choices and finally the right one
        test_number = '3'
        inputs = ['test', 'Y', '99', test_number]
        mock_inputs(inputs)
        result = functions.ask_number("test", 1, 10)

        self.assertTrue(result == int(test_number))

    def test_ask_list_of_numbers(self):
        # INPUTS
        #   Incorrect interleaved options, which will be ignored
        incorrect_test_numbers = '2,3,99,1,hola,4'
        expected_result = [2, 3, 1, 4]
        inputs = [incorrect_test_numbers]
        mock_inputs(inputs)
        result = functions.ask_list_of_numbers("test", 1, 10)

        self.assertTrue(result == expected_result)

    def test_ask_unique_name(self):
        test_name = 'TestName'
        repeat_name = 'Repeat'
        people = [Person(repeat_name), Person('Dani')]
        inputs = [repeat_name, test_name]
        mock_inputs(inputs)
        new_name = functions.ask_unique_name(people, 'test')

        self.assertEqual(new_name, test_name)

    @patch('briw.persistence.people_controller.update_user_in_database')
    def test_set_favourite_drink(self, update_user_in_database):

        person_id = '1'
        drink_id = '2'

        # INPUTS
        #   '1': person id in the people list
        #   '2': drink id in the drinks list
        input_values = [person_id, drink_id]
        mock_inputs(input_values)

        people = [Person('Julio'), Person('Dani')]
        drinks = [Drink('Water'), Drink('Coffee')]

        update_user_in_database.return_value = Person(
            people[int(person_id)-1].name, drinks[int(drink_id)-1].name, 12)

        people = functions.set_favourite_drink(people, drinks)

        self.assertTrue(people[0].name == 'Julio')
        self.assertTrue(people[0].favourite_drink.name == drinks[1].name)
        self.assertTrue(people[1].favourite_drink == None)

    @patch('briw.persistence.people_controller.save_new_user_in_database')
    def test_create_new_person_with_drink(self, save_new_user_in_database):
        # Select the first option to create
        test_name = ' TestName '
        drink_option = '1'

        # INPUTS
        # Julio: Repeated name to verify that it is not allowed to repeat name in the list of persons
        # TestName: Unique name
        # 'Y': option to select that I want to add the favorite drink of the new period.
        # '99': Incorrect number for the moment of choosing a drink from the list.
        # drinkOption: Correct number for the moment of choosing a drink from the list
        input_values = ['Julio', test_name, 'Y', '99', drink_option]
        mock_inputs(input_values)

        people = [Person('Julio'), Person('Dani')]
        drinks = [Drink('Water'), Drink('Coffee')]

        save_new_user_in_database.return_value = Person(
            test_name.strip(), drinks[int(drink_option)-1], 12)

        people = functions.create_new_person(people, drinks)

        self.assertTrue(len(people) == 3)
        self.assertTrue(people[-1].name == test_name.strip())
        self.assertTrue(
            people[-1].favourite_drink.name == drinks[int(drink_option)-1].name)

    @patch('briw.persistence.people_controller.save_new_user_in_database')
    def test_create_new_person_without_drink(self, save_new_user_in_database):
        # Select the first option to create
        test_name = ' TestName '
        person_id = 12

        # INPUTS
        # Julio: Repeated name to verify that it is not allowed to repeat name in the list of persons
        # TestName: Unique name
        # 'N': option to select that I don't want to add the favorite drink of the new period.
        # '99': Incorrect number for the moment of choosing a drink from the list.
        # drinkOption: Correct number for the moment of choosing a drink from the list
        input_values = ['Julio', 'TestName', 'N']
        mock_inputs(input_values)

        people = [Person('Julio'), Person('Dani')]
        drinks = [Drink('Water'), Drink('Coffee')]

        save_new_user_in_database.return_value = Person(
            test_name.strip(), person_id=person_id)

        people = functions.create_new_person(people, drinks)

        self.assertTrue(len(people) == 3)
        self.assertTrue(people[len(people)-1].name == test_name.strip())
        self.assertTrue(
            people[len(people)-1].favourite_drink == None)
        self.assertTrue(
            people[len(people)-1].person_id == person_id)

    @patch('briw.persistence.drinks_controller.save_new_drink_in_database')
    def test_add_drink(self, save_new_drink_in_database):
        new_drink_name = 'Beer'
        drink_id = 12
        drinks = [Drink('Water'), Drink('Coffee')]
        input_values = ['Water', new_drink_name]
        mock_inputs(input_values)

        save_new_drink_in_database.return_value = Drink(
            new_drink_name, drink_id=drink_id)

        new_drinks = functions.add_drink(drinks)

        self.assertTrue(len(new_drinks) == 3)
        self.assertTrue(drinks[-1].name == new_drink_name)
        self.assertTrue(drinks[-1].drink_id == drink_id)

    def test_not_allow_the_creation_of_a_round_if_an_open_one_already_exists(self):
        people = [Person('Julio'), Person('Dani')]
        rounds = [Round()]

        new_rounds = functions.create_round_and_set_brewer(people, rounds)

        self.assertEqual(rounds, new_rounds)

    @patch('briw.persistence.round_controller.create_new_open_round_in_database')
    def test_create_new_round_and_set_maker(self, create_new_open_round_in_database):

        maker_selected_id = '1'
        people = [Person('Julio'), Person('Dani')]
        rounds = [Round(is_open=False)]

        input_values = [maker_selected_id]
        mock_inputs(input_values)

        create_new_open_round_in_database.return_value = Round(
            brewer=people[int(maker_selected_id)-1])

        new_rounds = functions.create_round_and_set_brewer(people, rounds)

        self.assertTrue(len(new_rounds) == 2)
        self.assertTrue(new_rounds[-1].is_open)
        self.assertEqual(new_rounds[-1].brewer,
                         people[int(maker_selected_id)-1])

    @patch('briw.persistence.round_controller.add_order_to_round_in_database')
    def test_add_order_to_round(self, add_order_to_round_in_database):
        selected_person_id = '1'
        selected_drink_id = '1'
        people = [Person('Julio'), Person('Dani')]
        drinks = [Drink('Water'), Drink('Coffee')]
        rounds = [Round(brewer=people[0])]
        new_order = Order(people[int(selected_person_id)-1],
                          drinks[int(selected_drink_id)-1])
        orders = [new_order]
        expected_rounds = [Round(orders)]

        input_values = [selected_person_id, selected_drink_id]
        mock_inputs(input_values)

        add_order_to_round_in_database.return_value = new_order

        new_rounds = functions.add_order_to_round(people, drinks, rounds)

        self.assertTrue(
            new_rounds[-1].orders[-1].drink.name ==
            expected_rounds[-1].orders[-1].drink.name)

        self.assertTrue(
            new_rounds[-1].orders[-1].person.name ==
            expected_rounds[-1].orders[-1].person.name)

    @patch('briw.persistence.round_controller.close_round_in_database')
    def test_close_open_round(self, close_round_in_database):
        people = [Person('Julio'), Person('Dani')]
        rounds = [Round(brewer=people[0])]

        input_values = ['Y']
        mock_inputs(input_values)

        close_round_in_database.return_value = Round(
            is_open=False, brewer=people[0])

        new_rounds = functions.close_open_round(rounds)

        self.assertTrue(new_rounds[-1].brewer.name == people[0].name)
        self.assertTrue(new_rounds[-1].is_open == False)


if __name__ == '__main__':
    unittest.main()

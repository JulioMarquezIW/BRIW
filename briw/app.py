import sys
from briw.functions import functions
from briw.functions import file_functions
from briw.functions import printer_aux
from briw.data import texts
from briw.persistence import people_controller, drinks_controller, round_controller


def run():
    people = []
    drinks = []
    rounds = []

    # Default filepaths
    drinks_filepath = "briw/resources/drinks.txt"
    people_filepath = "briw/resources/people.txt"
    rounds_filepath = "briw/resources/rounds.txt"

    rounds = round_controller.get_rounds_from_database()
    people = people_controller.get_people_from_database()
    drinks = drinks_controller.get_drinks_from_database()

    # Read data from files
    # people = file_functions.read_people_from_file(people_filepath)
    # drinks = file_functions.read_drinks_from_file(drinks_filepath)
    # rounds = file_functions.read_rounds(rounds_filepath)

    # Check arguments
    functions.check_args(sys.argv, people, drinks)

    while True:
        # Print the available options
        printer_aux.print_options()

        minimumOptionNumber = 0
        maximumOptionNumber = 11

        # Ask for a value, which must be a number,
        # and repeat the question until the user enters a number.
        op = functions.ask_number(
            texts.ENTER_OPTION, minimumOptionNumber, maximumOptionNumber)

        if op == 1:
            # Print list of drinks
            printer_aux.print_list(texts.DRINKS, drinks)
        elif op == 2:
            # Print list of users
            printer_aux.print_list(texts.PEOPLE, people)
        elif op == 3:
            # Print list of users and preferences
            printer_aux.print_users_preferences(people)
        elif op == 4:
            # Call the function to follow the steps to add a new drink
            drinks = functions.add_drink(drinks)
        elif op == 5:
            # Call the function to follow the steps to add a new person
            people = functions.create_new_person(people, drinks)
        elif op == 6:
            # Set favourite drink
            people = functions.set_favourite_drink(people, drinks)
        elif op == 7:
            # Create a new round
            rounds = functions.create_round_and_set_brewer(people, rounds)
        elif op == 8:
            # Add order to round
            functions.add_order_to_round(people, drinks, rounds)
        elif op == 9:
            # Print rounds
            printer_aux.print_rounds(rounds)
        elif op == 10:
            # HELP MESSAGE
            print(texts.HELP_MESSAGE)
        elif op == 0 or op == None:
            # Just exit the program
            functions.goodbye(people, drinks, rounds,
                              people_filepath, drinks_filepath, rounds_filepath)
            exit()
        else:
            # If the number you entered is not in the options, ask for it again
            print(texts.INCORRECT_OPTION)
        printer_aux.enter_to_continue()

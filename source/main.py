import sys
import functions
import file_functions
import printer_aux
import texts

people = []
drinks = []

# Default filepaths
drinks_filepath = "data/drinks.txt"
people_filepath = "data/people.txt"

# Read data from files
people = file_functions.read_people_from_file(people_filepath)
drinks = file_functions.read_drinks_from_file(drinks_filepath)

# Check arguments
functions.check_args(sys.argv, people, drinks)

while True:
    # Print the available options
    printer_aux.print_options()

    minimumOptionNumber = 0
    maximumOptionNumber = 8

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
        functions.add_drink(drinks)
    elif op == 5:
        # Call the function to follow the steps to add a new person
        functions.create_new_person(people, drinks)
    elif op == 6:
        # Set favourite drink
        people = functions.set_favourite_drink(people, drinks)
    elif op == 7:
        # Create a new round
        print(texts.help_message)
    elif op == 8:
        # HELP MESSAGE
        print(texts.help_message)
    elif op == 0 or op == None:
        # Just exit the program
        functions.goodbye(people, drinks, people_filepath, drinks_filepath)
        exit()
    else:
        # If the number you entered is not in the options, ask for it again
        print(texts.INCORRECT_OPTION)
    printer_aux.enter_to_continue()

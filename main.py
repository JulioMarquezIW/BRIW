import sys
import functions
import file_functions
import printer_aux
import texts
import help_text

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

    # Ask for a value, which must be a number,
    # and repeat the question until the user enters a number.
    op = functions.ask_input_int(texts.ENTER_OPTION)

    if op == 1:
        # Print list of drinks
        printer_aux.print_list(texts.DRINKS, drinks)
    elif op == 2:
        # Print list of users
        printer_aux.print_users(people)
    elif op == 3:
        # Call the function to follow the steps to add a new drink
        functions.add_drink(drinks, drinks_filepath)
    elif op == 4:
        # Call the function to follow the steps to add a new person
        functions.create_new_person(people, people_filepath)
    elif op == 555:
        # Call the function to follow the steps to add a new person
        print(help_text.help_message)
    elif op == 0:
        # Just exit the program
        exit()
    else:
        # If the number you entered is not in the options, ask for it again
        print(texts.INCORRECT_OPTION)
    printer_aux.enter_to_continue()

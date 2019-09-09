
from person import Person
import printer_aux
import texts
import data
import file_functions
import help_text


def ask_input_string(text):
    # Auxiliary function to request a value(text) per command and check for errors.
    # +Parameters:
    #   - text: Message shown to request information
    #
    # Returns the value obtained

    error = True
    res = None
    while error:
        res = input(text)
        if not res:
            print(texts.NOT_EMPTY)
        else:
            error = False
    return res


def ask_input_int(text):
    # Auxiliary function to request a value(number) per command and check for errors.
    # +Parameters:
    #   - text: Message shown to request information
    #
    # Returns the value obtained

    error = True
    res = 0
    while error:
        try:
            res = int(input(text))
            error = False
        except ValueError:
            print(texts.ENTRY_INTEGER)
    return res


def add_drink():
    # Auxiliary function to ask and add a new drink, in cache and write in the file.

    drink = ask_input_string(texts.DRINK_NAME)
    file_functions.write_new_drink(drink)
    data.drinks.append(drink)


def create_new_person():
    # Requests by console the necessary information to create a new person,
    # which are, name and favourite drink. Finaly save this new person in
    # cache and write in the people file.

    name = ask_input_string(texts.ENTER_NAME)
    drink = ask_input_string(texts.ENTER_FAVOURITE_DRINK)
    p = Person(name, drink)
    file_functions.write_new_person(p)
    data.people.append(p)


def get_option():
    # Manages the control of the available options that can
    # be entered by the user through the terminal.

    # Ask for a value, which must be a number,
    # and repeat the question until the user enters a number.
    op = ask_input_int(texts.ENTER_OPTION)

    if op == 1:
        # Print list of drinks
        printer_aux.print_list(texts.DRINKS, data.drinks)
    elif op == 2:
        # Print list of users
        printer_aux.print_users()
    elif op == 3:
        # Call the function to follow the steps to add a new drink
        add_drink()
    elif op == 4:
        # Call the function to follow the steps to add a new person
        create_new_person()
    elif op == 555:
        # Call the function to follow the steps to add a new person
        print(help_text.help_message)
    elif op == 0:
        # Just exit the program
        exit()
    else:
        # If the number you entered is not in the options, ask for it again
        print(texts.INCORRECT_OPTION)
        get_option()


def args_options(arg):
    # Manage the events available to add as arguments when launching the project.
    # +Parameters:
    #   - arg: The argument received

    if arg == 'get-people':
        # Print a list of people
        printer_aux.print_users()
    elif arg == 'get-drinks':
        # Print a list of drinks
        printer_aux.print_list(texts.DRINKS, data.drinks)
    else:
        # If the received argument is not among those available,
        # an error message is printed and you exit the program.
        print(texts.AVAILABLE_ARGUMENTS_OPTIONS)
    exit()


def check_args(args):
    # Manage the number of received arguments. Only one argument is allow.
    # +Parameters:
    #   - args: The arguments received

    len_args = len(args)
    # The arguments must have a length of 2 because
    # the first one is the name of the file when invoking it.
    if len_args > 2:
        # Help message and exit
        print(texts.AVAILABLE_ARGUMENTS_OPTIONS)
        exit()
    elif len_args == 2:
        args_options(args[1])

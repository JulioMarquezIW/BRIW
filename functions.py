
from person import Person
import printer_aux
import texts
import data

# ========================= AUX FUNCTIONS =========================


def ask_input_string(text):
    # Auxiliary function to request a value per command and check for errors
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
    # Auxiliary function to request a value per command and check for errors
    error = True
    res = 0
    while error:
        i = input(text)


# ========================= FUNCTIONS =========================


def add_drink():
    drink = ask_input_string('Enter the drink name please: ')
    data.drinks.append(drink)


def create_new_person():
    # Requests by console the necessary information to create a new person
    print(texts.NEW_PERSON)
    name = ask_input_string(texts.ENTER_NAME)
    drink = ask_input_string(texts.ENTER_FAVOURITE_DRINK)
    data.people.append(Person(name, drink))


def get_option():
    op = None
    try:
        op = int(input("Enter the option: "))
    except ValueError:
        print("Please entry an integer.")
    if op == 1:
        printer_aux.print_list(texts.DRINKS, data.drinks)
    elif op == 2:
        printer_aux.print_users()
    elif op == 3:
        add_drink()
    elif op == 4:
        create_new_person()
    elif op == 0:
        exit()
    else:
        print("Incorrect option, please retry:")
        get_option()


def args_options(arg):
    if arg == 'get-people':
        printer_aux.print_users()
    elif arg == 'get-drinks':
        printer_aux.print_list(texts.DRINKS, data.drinks)
    else:
        print(texts.AVAILABLE_ARGUMENTS_OPTIONS)
    exit()


def check_args(args):
    # Requests by console the necessary information to create a new person
    len_args = len(args)
    if len_args > 2:
        print(texts.AVAILABLE_ARGUMENTS_OPTIONS)
        exit()
    elif len_args == 2:
        args_options(args[1])

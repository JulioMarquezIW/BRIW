
from drink import Drink
from person import Person
import printer_aux
import texts
import file_functions


def ask_boolean(text):
    """
    Auxiliary function to do a simple question to get YES or NO
    +Parameters:
        - text: Message shown to request information

    Returns a boolean in function of the text getted
    """
    error = True
    res = False
    while error:
        try:
            inp = input(text)
            if inp.upper() == "Y":
                res = True
                error = False
            elif inp.upper() == "N" or len(inp) == 0:
                res = False
                error = False
            else:
                print(texts.ENTRY_BOOLEAN)
        except ValueError:
            print(texts.ENTRY_BOOLEAN)
    return res


def ask_number(text, mininum, maximum):
    """
    Auxiliary function to request a value(number) per command and check for errors.
    +Parameters:
        - text: Message shown to request information
        - mininum: Minimum number allow
        - maximum: Maximum number allow

    Returns the value obtained
    """

    error = True
    res = 0
    while error:
        try:
            res = input(text)
            if len(res) != 0:
                res = int(res)
                if res > maximum or res < mininum:
                    print(texts.INCORRECT_OPTION)
                else:
                    error = False
            else:
                res = 0
                error = False
        except ValueError:
            print(texts.ENTRY_INTEGER)
    return res


def ask_unique_name(saved_list, text):
    """
    Check if the new element's of the list is not in the list
        +Parameters:
        - saved_list: List of all saved elements 
        - text: Message to show to ask the name
    Return True if the name is repeated
    """
    error = True
    name = None
    while error:
        name = input(text).strip()
        if len(name) != 0:
            if any(x.name.upper() == name.upper() for x in saved_list):
                print(texts.DUPLICATE_NAME)
            else:
                error = False
        else:
            error = False
    return name


def add_drink(drinks):
    """
    Auxiliary function to ask and add a new drink, in cache and write in the file.
    +Parameters:
        - drinks: list of drinks
    """

    drink = ask_unique_name(drinks, texts.DRINK_NAME)
    if len(drink) != 0:
        drinks.append(Drink(drink))


def create_new_person(people, drinks):
    """
    Requests by console the necessary information to create a new person,
    which are, name and favourite drink. Checks if this user already exists. 
    And finaly save this new person in cache and write in the people file.
    + Parameters:
        - people: list of people
        - drinks: list of drinks
    """

    drink = None
    name = ask_unique_name(people, texts.ENTER_NAME)
    if len(name) != 0:
        add_drink = ask_boolean(texts.QUESTION_ADD_DRINK)
        if add_drink:
            printer_aux.print_list(texts.DRINKS, drinks)
            drink_id = ask_number(texts.ENTER_DRINK_ID, 0, len(drinks))
            if drink_id != 0:
                drink = drinks[drink_id-1]

        p = Person(name, drink)
        people.append(p)


def args_options(arg, people, drinks):
    """
    Manage the events available to add as arguments when launching the project.
    +Parameters:
        - arg: The argument received
        - people: list of people
        - drinks: list of drinks
    """

    if arg == 'get-people':
        # Print a list of people
        printer_aux.print_list(texts.PEOPLE, people)
    elif arg == 'get-drinks':
        # Print a list of drinks
        printer_aux.print_list(texts.DRINKS, drinks)
    else:
        # If the received argument is not among those available,
        # an error message is printed and you exit the program.
        print(texts.AVAILABLE_ARGUMENTS_OPTIONS)
    exit()


def check_args(args, people, drinks):
    """
    Manage the number of received arguments. Only one argument is allow.
    +Parameters:
        - args: The arguments received
        - people: list of people
        - drinks: list of drinks
    """

    len_args = len(args)
    # The arguments must have a length of 2 because
    # the first one is the name of the file when invoking it.
    if len_args > 2:
        # Help message and exit
        print(texts.AVAILABLE_ARGUMENTS_OPTIONS)
        exit()
    elif len_args == 2:
        args_options(args[1], people, drinks)


def set_favourite_drink(people, drinks):
    """
    Set the person favourite drink
    + Parameters:
        - people: list of people
        - drinks: list of drinks
    """

    # Get Person ID
    printer_aux.print_list(texts.PEOPLE, people)
    person_id = ask_number(texts.ENTER_PERSON_ID, 0, len(people))
    if person_id != 0:
        printer_aux.print_list(texts.DRINKS, drinks)
        drink_id = ask_number(texts.ENTER_DRINK_ID, 0, len(drinks))
        if drink_id != 0:
            drink = drinks[drink_id-1]
            people[person_id - 1].set_favourite_drink(drink)
            print(texts.FAVOURITE_DRINK_UPDATED)
    return people


def goodbye(people, drinks, people_path, drink_path):
    """
    Function that is always executed when exiting the program
    + Parameters:
        - people: list of people
        - drinks: list of drinks
        - people_path: Path where to store the list of people
        - drink_path: Path where to store the list of drinks
    """
    if ask_boolean(texts.WANT_TO_SAVE):
        file_functions.write_drinks(drinks, drink_path)
        file_functions.write_people(people, people_path)
        print(texts.ALL_SAVED)
    print(texts.GOODBYE)


def create_round(people, drinks):
    """
    Function to create a new round, asking for what people want some drink]
    and what drink (Asking first if they want them favourite drink)
    + Parameters:
        - people: list of people
        - drinks: list of drinks
    """
    pass
    if ask_boolean(texts.ROUND_FAVOURITE_DRINKS):
        # TODO Round of the favourites
        pass
    elif ask_boolean(texts.ALL_PEOPLE_WANT_DRINKS):
        # TODO Round with all people
        pass
    else:
        pass
        # TODO Ask what people want a drink
        # TODO Round with the new list of people
        # TODO Ask if the people want their favorite drink

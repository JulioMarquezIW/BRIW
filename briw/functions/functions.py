
from briw.classes.drink import Drink
from briw.classes.person import Person
from briw.classes.brew_round import Round
from briw.classes.order import Order
from briw.functions import printer_aux
from briw.data import texts
from briw.functions import file_functions
from os import system
from briw.persistence import people_controller, drinks_controller, round_controller
from briw.database.database_execption import DatabaseError


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
            inp = str(input(text))
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


def ask_person_id(text, people):
    printer_aux.print_list(texts.PEOPLE, people)
    return ask_number(text, 0, len(people))


def ask_list_of_numbers(text, mininum, maximum):
    """
    Auxiliary function to request a list of numbers, checking that all of them al numbers.
    +Parameters:
        - text: Message shown to request information
        - mininum: Minimum number allow
        - maximum: Maximum number allow

    Returns the list of numbers
    """

    numbers = []

    temp_list = input(text).strip().split(',')
    for element in temp_list:
        try:
            num = int(element)
            if num > maximum or num < mininum:
                print(f"{element} is out of the range. Value omitted.")
            else:
                numbers.append(num)

        except ValueError:
            print(f"{element} is not a number. Value omitted.")

    return numbers


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

    drink_name = ask_unique_name(drinks, texts.DRINK_NAME)
    if len(drink_name) != 0:

        try:
            drink_saved = drinks_controller.save_new_drink_in_database(
                Drink(drink_name))
            drinks.append(drink_saved)
        except DatabaseError:
            print('Database error, new drink will not be saved')

    return drinks


def ask_drink_in_list(drinks, text):
    """
    Show the list of the drinks and ask for one id of them
    + Parameters:
        - drinks: list of drinks
    """
    printer_aux.print_list(texts.DRINKS, drinks)
    drink_id = ask_number(text, 0, len(drinks))
    return drink_id


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
            drink_id = ask_drink_in_list(drinks, texts.ENTER_DRINK_ID)
            if drink_id != 0:
                drink = drinks[drink_id-1]
        p = Person(name, drink)
        try:
            saved_person = people_controller.save_new_user_in_database(p)
            people.append(saved_person)
        except DatabaseError:
            print('Database error, new user will not be saved')

    return people


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
    person_id = ask_person_id(texts.ENTER_PERSON_ID, people)
    if person_id != 0:
        printer_aux.print_list(texts.DRINKS, drinks)
        drink_id = ask_number(texts.ENTER_DRINK_ID, 0, len(drinks))
        if drink_id != 0:
            drink = drinks[drink_id-1]
            person_to_save = people[person_id - 1]
            person_to_save.set_favourite_drink(drink)
            try:
                people_controller.update_user_in_database(person_to_save)
                people[person_id - 1].set_favourite_drink(drink)
                print(texts.FAVOURITE_DRINK_UPDATED)
            except DatabaseError:
                print('Database error, favourite drink will not be setted')

    return people


def goodbye(people, drinks, rounds, people_path, drink_path, round_path):
    """
    Function that is always executed when exiting the program
    + Parameters:
        - people: list of people
        - drinks: list of drinks
        - people_path: Path where to store the list of people
        - drink_path: Path where to store the list of drinks
    """
    # if ask_boolean(texts.WANT_TO_SAVE):
    #     file_functions.write_drinks(drinks, drink_path)
    #     file_functions.write_people(people, people_path)
    #     file_functions.write_rounds(rounds, round_path)
    #     print(texts.ALL_SAVED)
    print(texts.GOODBYE)


def ask_drinks_for_pepole(new_round, people, drinks):
    """
    Ask for the drink that each person wants from the list of people passed as parameter.
    + Parameters:
        - new_round: round that is being created
        - people: list of people who wants a drink
        - drinks: list of drinks
    Returns the received round filled with the orders that have been correctly entered.
    """
    for person in people:
        system('clear')
        text = ""
        if person.favourite_drink:
            text = f"Enter the drink ID for {person.name} \n His favourite drink is {person.favourite_drink.name}. (0) if this person doesn't want a drink: "
        else:
            text = f"Enter the drink ID for {person.name}, (0) if this person doesn't want a drink: "
        drink_id = ask_drink_in_list(drinks, text)
        if drink_id != 0:
            new_round.add_order(person, drinks[drink_id-1])
    return new_round


def ask_sublist_people(people, drinks, new_round):
    """
    Show the list of the people and ask what people want in a new list.
    + Parameters:
        - people: list of people
        - text: text to show in console
    Return a new people list
    """

    system('clear')
    printer_aux.print_list(texts.PEOPLE, people)
    new_people_list = []
    identifiers = ask_list_of_numbers(texts.ASK_PEOPLE_IDS, 1, len(people))

    for p_id in identifiers:
        new_people_list.append(people[p_id-1])

    printer_aux.print_list(texts.PEOPLE_WHO_WANT_DRINK, new_people_list)
    printer_aux.enter_to_continue()

    return ask_drinks_for_pepole(new_round, new_people_list, drinks)


def create_round(people, drinks):
    """
    Function to create a new round, asking for what people want some drink]
    and what drink (Asking first if they want them favourite drink)
    + Parameters:
        - people: list of people
        - drinks: list of drinks
    """
    system('clear')
    new_round = Round()
    new_round.orders = []

    brewer_id = ask_person_id(texts.ASK_BREWER, people)

    if brewer_id != 0:
        new_round.brewer = people[brewer_id-1]

        people_without_favorite = []
        if ask_boolean(texts.ROUND_FAVOURITE_DRINKS):
            for person in people:
                if person.favourite_drink:
                    new_round.add_order(person, person.favourite_drink)
                else:
                    people_without_favorite.append(person)
            if people_without_favorite:
                system('clear')
                print(texts.PEOPLE_WITHOUT_FAVOURITE_DRINK)
                printer_aux.print_list(texts.PEOPLE, people_without_favorite)
                printer_aux.enter_to_continue()
                new_round = ask_drinks_for_pepole(
                    new_round, people_without_favorite, drinks)
        elif ask_boolean(texts.ALL_PEOPLE_WANT_DRINKS):
            new_round = ask_drinks_for_pepole(new_round, people, drinks)
        else:
            new_round = ask_sublist_people(people, drinks, new_round)

    new_round.print_round()
    return new_round


def create_round_and_set_brewer(people, rounds):
    system('clear')

    if rounds[-1].is_open:
        print(texts.OPEN_ROUND_INFO)
    else:
        new_round = Round()

        brewer_id = ask_person_id(texts.ASK_BREWER, people)

        if brewer_id != 0:
            new_round.brewer = people[brewer_id-1]

            try:
                new_round = round_controller.create_new_open_round_in_database(
                    new_round)
                rounds.append(new_round)
                print(texts.CREATED_ROUND)
                print(texts.FAVOURITE_DRINK_UPDATED)
            except DatabaseError:
                print(texts.DATABASE_ERROR + texts.ROUND_NOT_ADDED)

    return rounds


def add_order_to_round(people, drinks, rounds):

    # open_rounds = round_controller.get_rounds_from_database(1)
    open_round = rounds[-1]

    if open_round.is_open:
        printer_aux.print_rounds([open_round])
        person_id = ask_person_id(texts.ENTER_PERSON_ID, people)
        if person_id != 0:
            printer_aux.print_list(texts.DRINKS, drinks)
            drink_id = ask_number(texts.ENTER_DRINK_ID, 0, len(drinks))
            if drink_id != 0:
                drink = drinks[drink_id-1]
                person = people[person_id - 1]
                new_order = Order(person, drink)
                try:
                    round_controller.add_order_to_round_in_database(
                        open_round, new_order)
                    rounds[-1].orders.append(new_order)
                    print(texts.CREATED_ORDER)
                except DatabaseError:
                    print(texts.DATABASE_ERROR + texts.ORDER_NOT_ADDED)
    else:
        print(texts.NOT_OPEN_ROUND)

    return rounds


def close_open_round(rounds):

    if rounds[-1].is_open:
        # open_rounds = round_controller.get_rounds_from_database(1)
        open_round = rounds[-1]
        printer_aux.print_rounds([open_round])

        if ask_boolean(texts.CONFIRM_CLOSE_ROUND):
            try:
                round_controller.close_round_in_database(open_round)
                rounds[-1].is_open = False
                print(texts.ROUND_CLOSED)
            except DatabaseError:
                print(texts.DATABASE_ERROR + texts.ROUND_NOT_CLOSED)

    else:
        print(texts.NOT_OPEN_ROUND)

    return rounds


from briw.classes.person import Person
from briw.classes.brew_round import Round
from briw.classes.order import Order
from briw.classes.drink import Drink
from briw.functions import printer_aux
from briw.data import texts
from datetime import datetime


def error_opening_file():
    print(texts.ERROR_FILE)
    printer_aux.enter_to_continue()


def read_people_from_file(filepath):
    people = []
    try:
        with open(filepath, "r") as people_file:
            for person in people_file.readlines():
                line = person.split(":")
                drink = None
                if line[1].strip() != 'None':
                    drink = Drink(line[1].strip())
                people.append(Person(line[0], drink))
    except FileNotFoundError as filenotfound:
        print(
            f"Could no open the file {filepath}. /nError: {str(filenotfound)}")
        error_opening_file()
    except Exception as e:
        print(
            f"Error opening the file {filepath}. /nError: {str(e)}")
        error_opening_file()

    return people


def read_drinks_from_file(filepath):
    drinks = []
    try:
        with open(filepath, "r") as drinks_file:
            for drink in drinks_file.readlines():
                drinks.append(Drink(drink.strip()))
    except FileNotFoundError as filenotfound:
        print(
            f"Could no open the file {filepath}. /nError: {str(filenotfound)}")
        error_opening_file()
    except Exception as e:
        print(
            f"Error opening the file {filepath}. /nError: {str(e)}")
        error_opening_file()

    return drinks


def read_rounds(filepath):
    rounds = []
    try:
        with open(filepath, "r") as rounds_file:
            for line in rounds_file.readlines():
                orders = line.strip().split(";")
                date = datetime.strptime(orders[0], texts.DATE_FORMAT)
                brewer = orders[1]
                round_orders = []
                for order in orders[2:]:
                    _order = order.split(",")
                    round_orders.append(
                        Order(Person(_order[0]), Drink(_order[1])))

                rounds.append(Round(round_orders, date, Person(brewer)))
    except FileNotFoundError as filenotfound:
        print(
            f"Could no open the file {filepath}. /nError: {str(filenotfound)}")
        error_opening_file()
    except Exception as e:
        print(
            f"Error opening the file {filepath}. /nError: {str(e)}")
        error_opening_file()

    return rounds


def write_drinks(drinks, filepath):
    try:
        with open(filepath, "w+") as drinks_file:
            for drink in drinks:
                drinks_file.write(f"{drink.name}\n")
    except FileNotFoundError as filenotfound:
        print(
            f"Could no open the file {filepath}. /nError: {str(filenotfound)}")
    except Exception as e:
        print(
            f"Error opening the file {filepath}. /nError: {str(e)}")


def write_people(people, filepath):
    try:
        with open(filepath, "w+") as people_file:
            for person in people:
                drink = "None"
                if person.favourite_drink:
                    drink = person.favourite_drink.name
                people_file.write(
                    f"{person.name}:{drink}\n")
    except FileNotFoundError as filenotfound:
        print(
            f"Could no open the file {filepath}. /nError: {str(filenotfound)}")
    except Exception as e:
        print(
            f"Error opening the file {filepath}. /nError: {str(e)}")


def write_rounds(rounds, filepath):

    rows = []
    for _round in rounds:
        row_to_write = ""
        # semi colon (;) used for seperation
        row_to_write += _round.open_date.strftime(texts.DATE_FORMAT)
        row_to_write += ";" + _round.brewer.name
        for order in _round.orders:
            row_to_write += f";{order.person.name},{order.drink.name}"

        row_to_write += "\n"
        rows.append(row_to_write)

    try:
        with open(filepath, "w+") as rounds_file:
            for row in rows:
                rounds_file.write(row)
    except FileNotFoundError as filenotfound:
        print(
            f"Could no open the file {filepath}. /nError: {str(filenotfound)}")
    except Exception as e:
        print(
            f"Error opening the file {filepath}. /nError: {str(e)}")

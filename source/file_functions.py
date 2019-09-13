
from person import Person
from drink import Drink
import printer_aux
import texts
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
    return []
    # try:
    #     with open(filepath, "r") as rounds_file:
    #         for line in rounds_file.readlines():
    #             orders = line.split(";")
    #             date = datetime.strptime(orders[0], "%y-%m-%d %H:%M:%S")

    #             for order in orders[1:]:
    #                 _order = order.split(",")
    #                 p_name = _order[0]
    #                 d_name = _order[1]

    #                 person = Person(p_name)
    #                 drink = Drink(d_name)


def write_drinks(drinks, filepath):
    try:
        with open(filepath, "w") as drinks_file:
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
        with open(filepath, "w") as people_file:
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
    try:
        with open(filepath, "w") as rounds_file:
            for _round in rounds:
                row_to_write = ""
                # semi colon (;) used for seperation
                row_to_write += _round.date.strftime("%y-%m-%d %H:%M:%S") + ";"
                for order in _round.orders:
                    row_to_write += f"{order.person.name},{order.drink.name};"

                row_to_write += "\n"
                rounds_file.write(row_to_write)
    except FileNotFoundError as filenotfound:
        print(
            f"Could no open the file {filepath}. /nError: {str(filenotfound)}")
    except Exception as e:
        print(
            f"Error opening the file {filepath}. /nError: {str(e)}")

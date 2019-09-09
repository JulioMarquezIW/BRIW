
from person import Person
import printer_aux
import texts


def error_opening_file():
    print(texts.ERROR_FILE)
    printer_aux.enter_to_continue()


def read_people_from_file(filepath):
    people = []
    try:
        with open(filepath, "r") as people_file:
            for person in people_file.readlines():
                line = person.split(":")
                people.append(Person(line[0], line[1].strip()))
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
                drinks.append(drink.strip())
    except FileNotFoundError as filenotfound:
        print(
            f"Could no open the file {filepath}. /nError: {str(filenotfound)}")
        error_opening_file()
    except Exception as e:
        print(
            f"Error opening the file {filepath}. /nError: {str(e)}")
        error_opening_file()

    return drinks


def write_new_drink(drink, filepath):
    try:
        with open(filepath, "a") as drinks_file:
            drinks_file.write(f"{drink}\n")
    except FileNotFoundError as filenotfound:
        print(
            f"Could no open the file {filepath}. /nError: {str(filenotfound)}")
    except Exception as e:
        print(
            f"Error opening the file {filepath}. /nError: {str(e)}")


def write_new_person(person: Person, filepath):
    filepath = "data/people.txt"
    try:
        with open(filepath, "a") as people_file:
            people_file.write(f"{person.name}:{person.favourite_drink}\n")
    except FileNotFoundError as filenotfound:
        print(
            f"Could no open the file {filepath}. /nError: {str(filenotfound)}")
    except Exception as e:
        print(
            f"Error opening the file {filepath}. /nError: {str(e)}")

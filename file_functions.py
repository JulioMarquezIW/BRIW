
from person import Person
import printer_aux
import data
import texts


def read_people_from_file():
    people = []
    f = open("data/people.txt", "r")
    for i in f.readlines():
        line = i.split(":")
        people.append(Person(line[0], line[1].strip()))
    data.people = people
    f.close()


def read_drinks_from_file():
    drinks = []
    f = open("data/drinks.txt", "r")
    for i in f.readlines():
        drinks.append(i.strip())
    data.drinks = drinks
    f.close()
    printer_aux.print_list(texts.DRINKS, drinks)


def read_data_from_files():
    read_drinks_from_file()
    read_people_from_file()


# read_people_from_file()
# printer_aux.print_users()
# read_drinks_from_file()

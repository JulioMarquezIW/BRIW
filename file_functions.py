
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


def read_data_from_files():
    read_drinks_from_file()
    read_people_from_file()


def write_new_drink(drink):
    f = open("data/drinks.txt", "a")
    f.write(f"{drink}\n")
    f.close()


def write_new_person(person: Person):
    f = open("data/people.txt", "a")
    f.write(f"{person.name}:{person.favourite_drink}\n")
    f.close()


# read_people_from_file()
# printer_aux.print_users()
# read_drinks_from_file()
# write_new_drink("Gin")
# write_new_person(Person("Henry", "Coffee"))



from os import system
import texts
import data


def print_divider():
    print(f"+{'=' * 30}+")


def print_options():
    system('clear')
    print_divider()
    print(texts.OPTIONS)
    print_divider()


def print_list(title, elements):
    print_divider()
    print('| ' + title.upper())
    print_divider()
    for l in elements:
        print('| ' + l)
    print_divider()
    print('\n')


def print_users():
    print_divider()
    print('| ' + texts.PEOPLE.upper() + ' | ' + texts.DRINKS.upper())
    print_divider()
    for p in data.people:
        print(f"| {p.name} | {p.typical_drink}")
    print_divider()
    print('\n')


def enter_to_continue():
    input(texts.PRESS_ENTER)

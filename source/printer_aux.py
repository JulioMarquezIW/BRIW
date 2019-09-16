from os import system
import texts
import functions


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
    for idx, l in enumerate(elements):
        print(f"| {idx+1}   | {l.name}")
    print_divider()
    print('\n')


def print_users_preferences(people):
    print_divider()
    print('| ' + texts.PEOPLE.upper() + ' | ' + texts.DRINKS.upper())
    print_divider()
    for idx, p in enumerate(people):
        print(
            f"| {idx+1}   | {p.name} | {p.favourite_drink.name if p.favourite_drink != None else texts.NOT_FAVOURITE_DRINK}")
    print_divider()
    print('\n')


def enter_to_continue(text=texts.PRESS_ENTER):
    input(texts.PRESS_ENTER)


def print_rounds(rounds):
    system('clear')
    print_divider()
    print('| ' + texts.ROUNDS.upper() + ' | ')
    print_divider()
    if len(rounds) != 0:
        rounds.reverse()
        i = 0
        for idx, r in enumerate(rounds):
            print('| ' + texts.ROUND_ID.upper() +
                  " : "+str(idx) + ' | ')
            print('| ' + texts.ROUND_DATE.upper() +
                  r.date.strftime(texts.DATE_FORMAT) + ' | ')
            print('| ' + texts.BREWER.upper() + " -> " +
                  r.brewer.name + ' | ')
            print('| ' + texts.PEOPLE.upper() + ' | ' + texts.DRINKS.upper())
            for idx, r in enumerate(r.orders):
                print(
                    f"| {idx+1}   | {r.person.name} | {r.drink.name}")
            print_divider()
            print("\n")
            i += 1
            if i % 2 == 0:
                if not functions.ask_boolean(texts.MORE_ROUNDS):
                    return
                else:
                    system('clear')
                    print_divider()
        print_divider()
    else:
        print('| '+texts.NO_ROUNDS.upper() + ' | \n')

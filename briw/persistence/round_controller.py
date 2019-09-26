
from briw.database.database import Database
from briw.database.database import Config
from briw.classes.brew_round import Round
from briw.functions.printer_aux import print_rounds
from briw.classes.person import Person
from briw.classes.order import Order
from briw.classes.drink import Drink


def get_rounds_from_database():
    rounds = []

    db = Database(Config)

    # SELECT * FROM BrewRound as b INNER JOIN BrewOrder as o ON o.round_id = b.round_id;
    db_rounds = db.run_query(
        """
        SELECT b.is_open, b.brewer as brewer_id, b.open_date, b.round_id, 
        p.name as person_name, d.name as drink_name, p2.name as brewer_name
        FROM julio.BrewRound as b 
        INNER JOIN BrewOrder as o 
        ON o.round_id = b.round_id 
        INNER JOIN Person as p 
        ON o.person_id = p.person_id
        INNER JOIN Person as p2 
        ON b.brewer = p2.person_id
        INNER JOIN Drink as d 
        ON o.drink_id = d.drink_id
        ORDER BY b.round_id;
        """)

    # TODO IMPROVE
    curret_round = db_rounds[0]
    round_orders = []
    rounds = []
    for idx, order in enumerate(db_rounds):
        if curret_round['round_id'] != order['round_id'] or idx == len(db_rounds):
            rounds.append(
                Round(round_orders, curret_round['open_date'], Person(curret_round['brewer_name'], None, curret_round['brewer_id']), curret_round['is_open']))
            curret_round = order
            round_orders = []
        round_orders.append(
            Order(Person(order['person_name']), Drink(order['drink_name'])))

    rounds.append(
        Round(round_orders, curret_round['open_date'], Person(curret_round['brewer_name'], None, curret_round['brewer_id']), curret_round['is_open']))

    return rounds


def create_new_open_round_in_database(new_round: Round):
    db = Database(Config)
    new_round.round_id = db.run_query(
        f"""
        INSERT INTO BrewRound(is_open,brewer, open_date)
        VALUES ({new_round.is_open},'{new_round.brewer.person_id}', 
        '{new_round.open_date.strftime('%Y-%m-%d %H:%M:%S')}')
        """)
    return new_round


# def delete_drink_in_database(drink: Drink):
#     db = Database(Config)
#     db.run_query(
#         f"""DELETE FROM Drink WHERE drink_id={drink.drink_id}""")


# def update_drink_in_database(drink: Drink):
#     db = Database(Config)
#     db.run_query(
#         f"""UPDATE Drink
#         SET name='{drink.name}', drink_id={drink.drink_id}
#         WHERE drink_id={drink.drink_id}
#         """)

new_round = Round()
p = Person('Julio', None, 1)
new_round.brewer = p

create_new_open_round_in_database(new_round)

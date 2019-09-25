
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

    orders = {}
    curret_round = db_rounds[0]['round_id']
    orders[curret_round] = []
    for order in db_rounds:
        if curret_round != order['round_id']:
            curret_round = order['round_id']
            orders[curret_round] = []
        orders[curret_round].append(order)

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
    print_rounds(rounds)

    return rounds


# def save_new_drink_in_database(new_drink: Drink):
#     db = Database(Config)
#     new_drink.drink_id = db.run_query(
#         f"""INSERT INTO Drink(name)
#         VALUES ('{new_drink.name}')""")
#     return new_drink


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

get_rounds_from_database()


from briw.database.database import Database
from briw.database.database import Config
from briw.classes.brew_round import Round
from briw.classes.person import Person
from briw.classes.order import Order
from briw.classes.drink import Drink


def get_rounds_from_database(is_open_filter=None):
    rounds = []

    db = Database(Config)

    query = """
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
        """

    if is_open_filter != None and isinstance(is_open_filter, bool):
        query += f" WHERE b.is_open={int(is_open_filter)}"

    query += " ORDER BY b.round_id"

    db_rounds = db.run_query(query)

    # TODO IMPROVE
    curret_round = db_rounds[0]
    round_orders = []
    rounds = []
    for idx, order in enumerate(db_rounds):
        if curret_round['round_id'] != order['round_id'] or idx == len(db_rounds):
            rounds.append(
                Round(
                    round_orders, curret_round['open_date'],
                    Person(curret_round['brewer_name'],
                           None, curret_round['brewer_id']),
                    curret_round['is_open'],
                    curret_round['round_id']))
            curret_round = order
            round_orders = []
        round_orders.append(
            Order(Person(order['person_name']), Drink(order['drink_name'])))

    rounds.append(
        Round(
            round_orders, curret_round['open_date'],
            Person(curret_round['brewer_name'],
                   None, curret_round['brewer_id']),
            curret_round['is_open'],
            curret_round['round_id']))

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


def add_order_to_round_in_database(open_round: Round, new_order: Order):
    db = Database(Config)

    db.run_query(
        f"""
        INSERT INTO BrewOrder(drink_id, person_id, round_id) 
        VALUES ({new_order.drink.drink_id},{new_order.person.person_id},{open_round.round_id})
        """)


def close_round_in_database(open_round: Round):
    db = Database(Config)

    db.run_query(
        f"""
        UPDATE BrewRound SET is_open=FALSE WHERE round_id={open_round.round_id}
        """)
    open_round.is_open = False

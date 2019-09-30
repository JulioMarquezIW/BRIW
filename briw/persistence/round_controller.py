
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
       	SELECT r.is_open, r.brewer as brewer_id, r.open_date, r.round_id,
        p.name as brewer_name, p2.name as person_name, d.name as drink_name,
        d.drink_id, p2.person_id, o.order_id
       	FROM BrewOrder as o
       	RIGHT JOIN BrewRound as r
       	ON o.round_id = r.round_id
        INNER JOIN Person as p 
        ON p.person_id = r.brewer
       	LEFT JOIN Drink as d 
        ON d.drink_id = o.drink_id
        LEFT JOIN Person as p2 
        ON p2.person_id = o.person_id
        """

    if is_open_filter != None and isinstance(is_open_filter, bool):
        query += f" WHERE r.is_open={int(is_open_filter)}"

    query += " ORDER BY r.round_id"

    db_rounds = db.run_query(query)

    rounds = []
    if len(db_rounds) != 0:
        curret_round = db_rounds[0]
        round_orders = []
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
            if order['person_name']:
                round_orders.append(
                    Order(Person(order['person_name'], person_id=order['person_id']),
                          Drink(order['drink_name'], order['drink_id']), order['order_id']))

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

    new_order.order_id = db.run_query(
        f"""
        INSERT INTO BrewOrder(drink_id, person_id, round_id) 
        VALUES ({new_order.drink.drink_id},{new_order.person.person_id},{open_round.round_id})
        """)
    return new_order


def close_round_in_database(open_round: Round):
    db = Database(Config)

    db.run_query(
        f"""
        UPDATE BrewRound SET is_open=FALSE WHERE round_id={open_round.round_id}
        """)
    open_round.is_open = False
    return open_round

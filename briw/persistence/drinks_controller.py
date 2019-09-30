
from briw.database.database import Database
from briw.database.database import Config
from briw.classes.drink import Drink


def get_drinks_from_database():
    drinks = []

    db = Database(Config)

    db_drinks = db.run_query(
        """SELECT * FROM Drink""")

    for drink in db_drinks:
        drinks.append(Drink(drink['name'], drink['drink_id']))

    return drinks


def save_new_drink_in_database(new_drink: Drink):
    db = Database(Config)
    new_drink.drink_id = db.run_query(
        f"""INSERT INTO Drink(name) 
        VALUES ('{new_drink.name}')""")
    return new_drink


def delete_drink_in_database(drink: Drink):
    db = Database(Config)
    db.run_query(
        f"""DELETE FROM Drink WHERE drink_id={drink.drink_id}""")


def update_drink_in_database(drink: Drink):
    db = Database(Config)
    db.run_query(
        f"""UPDATE Drink
        SET name='{drink.name}', drink_id={drink.drink_id}
        WHERE drink_id={drink.drink_id}
        """)


def get_drink_by_id_from_database(drink_id):

    db = Database(Config)

    db_drinks = db.run_query(
        f"""SELECT * FROM Drink AS d WHERE d.drink_id = {drink_id} """)

    if len(db_drinks) != 0:
        drink = db_drinks[0]
        return Drink(drink['name'], drink['drink_id'])
    else:
        return None

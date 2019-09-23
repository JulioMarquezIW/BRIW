
from briw.database.database import Database
from briw.database.database import Config
from briw.classes.person import Person
from briw.classes.drink import Drink


def test():
    print(Config.db_host)
    db = Database(Config)
    users = db.run_query(
        """SELECT p.person_id, p.name as person_name, p.favorite_drink_id, d.name as drink_name 
        FROM Person AS p INNER JOIN Drink as d ON p.favorite_drink_id = d.drink_id""")

    for user in users:
        print(user)


def get_people_from_database():
    users = []

    db = Database(Config)
    # SELECT p.person_id, p.name as person_name, p.favorite_drink_id, d.name as drink_name  FROM Person AS p INNER JOIN Drink as d ON p.favorite_drink_id = d.drink_id
    db_users = db.run_query(
        """SELECT p.person_id, p.name as person_name, p.favorite_drink_id, d.name as drink_name 
        FROM Person AS p INNER JOIN Drink as d ON p.favorite_drink_id = d.drink_id""")

    for user in db_users:
        users.append(Person(user[1], Drink(user[2], user[3])))

    return users

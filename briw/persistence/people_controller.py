
from briw.database.database import Database
from briw.database.database import Config
from briw.classes.person import Person
from briw.classes.drink import Drink


def get_people_from_database():
    users = []

    db = Database(Config)

    db_users = db.run_query(
        """SELECT p.person_id, p.name as person_name, p.favorite_drink_id, d.name as drink_name 
        FROM Person AS p INNER JOIN Drink as d ON p.favorite_drink_id = d.drink_id""")

    for user in db_users:
        users.append(Person(user[1], Drink(user[2], user[3])))

    return users


def save_new_user_in_database(new_user: Person):
    db = Database(Config)
    db.run_query(
        f"""INSERT INTO Person(name,favorite_drink_id) 
        VALUES ('{new_user.name}', {new_user.favourite_drink.drink_id})""")


def delete_user_in_database(user: Person):
    db = Database(Config)
    db.run_query(
        f"""DELETE FROM Person WHERE person_id={user.person_id}""")


def update_user_in_database(user: Person):
    db = Database(Config)
    db.run_query(
        f"""UPDATE Person
        SET name='{user.name}', favourite_drink_id={user.favourite_drink.drink_id}
        WHERE person_id={user.person_id}
        """)


# drink = Drink('testdrink', 1)
# user = Person('test', drink, 3)

# update_user_in_database(user)

# delete_user_in_database(user)

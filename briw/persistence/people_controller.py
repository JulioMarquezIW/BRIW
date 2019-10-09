
from briw.database.database import Database
from briw.database.database import Config
from briw.classes.person import Person
from briw.classes.drink import Drink


def get_people_from_database():
    users = []

    db = Database(Config)

    db_users = db.run_query(
        """SELECT p.person_id, p.name as person_name, p.favourite_drink_id, d.name as drink_name
        FROM Person AS p LEFT JOIN Drink as d ON p.favourite_drink_id = d.drink_id""")

    for user in db_users:
        users.append(Person(user['person_name'], Drink(
            user['drink_name'], user['favourite_drink_id']), user['person_id']))

    return users


def save_new_user_in_database(new_user: Person):
    db = Database(Config)
    query = f"""INSERT INTO Person(name) VALUES ('{new_user.name}')"""

    if new_user.favourite_drink != None:
        query = f"""INSERT INTO Person(name,favourite_drink_id)
        VALUES ('{new_user.name}', {new_user.favourite_drink.drink_id})"""

    new_user.person_id = db.run_query(query)
    return new_user


def delete_user_in_database(person: Person):
    db = Database(Config)
    db.run_query(
        f"""DELETE FROM Person WHERE person_id={person.person_id}""")


def update_user_in_database(person: Person):
    db = Database(Config)

    if person.favourite_drink == None:
        query = f"""UPDATE Person 
        SET name='{person.name}', favourite_drink_id=NULL"""
    else:
        query = f"""UPDATE Person 
        SET name='{person.name}', favourite_drink_id={person.favourite_drink.drink_id}"""

    query += f""" WHERE person_id={person.person_id}"""
    db.run_query(query)


def get_person_by_id_from_database(person_id):

    db = Database(Config)

    db_users = db.run_query(
        f"""SELECT p.person_id, p.name as person_name, p.favourite_drink_id, d.name as drink_name
        FROM Person AS p INNER JOIN Drink as d ON p.favourite_drink_id = d.drink_id WHERE p.person_id = {person_id} """)

    if len(db_users) != 0:
        user = db_users[0]
        return Person(user['person_name'], Drink(
            user['drink_name'], user['favourite_drink_id']), user['person_id'])
    else:
        return None


def search_person_by_name(person_name):
    db = Database(Config)

    people = []

    db_users = db.run_query(
        f"""SELECT p.person_id, p.name as person_name, p.favourite_drink_id, d.name as drink_name
        FROM Person AS p INNER JOIN Drink as d ON p.favourite_drink_id = d.drink_id WHERE upper(p.name) = '{person_name.strip().upper()}' """)

    if len(db_users) != 0:
        for user in db_users:
            people.append(Person(user['person_name'], Drink(
                user['drink_name'], user['favourite_drink_id']), user['person_id']))

    return people


def get_people_by_favourite_drink_from_database(drink_id):

    db = Database(Config)

    db_people = db.run_query(
        f"""SELECT p.person_id, p.name as person_name, p.favourite_drink_id, d.name as drink_name
        FROM Person AS p INNER JOIN Drink as d ON p.favourite_drink_id = d.drink_id WHERE p.favourite_drink_id = {drink_id} """)

    people = []
    for person in db_people:
        people.append(Person(person['person_name'], Drink(
            person['drink_name'], person['favourite_drink_id']), person['person_id']))
    return people

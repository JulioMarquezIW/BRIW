
from briw.database.database import Database
from briw.database.database import Config


def test():
    print(Config.db_host)
    db = Database(Config)
    users = db.run_query("SELECT * FROM Person")

    for user in users:
        print(user)

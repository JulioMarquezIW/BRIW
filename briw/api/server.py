
# from encoder import *
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from briw.persistence.drinks_controller import get_drinks_from_database, save_new_drink_in_database
from briw.persistence.people_controller import get_people_from_database, save_new_user_in_database
from briw.persistence.round_controller import get_rounds_from_database
from briw.classes.drink import Drink
from briw.classes.person import Person
from briw.api.drink_encoder import DrinkEncoder
from briw.database.database_execption import DatabaseError
from briw.api.people_encoder import PeopleEncoder
from briw.api.round_encoder import RoundEncoder


def get_drinks():
    drinks = get_drinks_from_database()
    return json.dumps(drinks, cls=DrinkEncoder)


def get_people():
    people = get_people_from_database()
    return json.dumps(people, cls=PeopleEncoder)


def get_rounds(round_filter=None):
    rounds = get_rounds_from_database(round_filter)
    return json.dumps(rounds, cls=RoundEncoder)


def post_drink(handler, data):
    try:
        new_drink = Drink(data["name"])
        save_new_drink_in_database(new_drink)
        handler.send_response(201)
    except KeyError as e:
        print("JSON KEY ERRORS: "+str(e))
        handler.send_response(400)
    except DatabaseError:
        handler.send_response(500)
        print('Database error, new drink will not be saved')
    finally:
        handler.end_headers()


def post_people(handler, data):
    try:
        new_person = Person(
            data['name'], Drink('', data['favourite_drink_id']))
        save_new_user_in_database(new_person)
        handler.send_response(201)
    except KeyError as e:
        print("JSON KEY ERRORS: "+str(e))
        handler.send_response(400)
    except DatabaseError:
        handler.send_response(500)
        print('Database error, new drink will not be saved')
    finally:
        handler.end_headers()


class APIHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.end_headers()

    def do_GET(self):
        self._set_headers()

        jd = {}
        if self.path == '/drinks':
            jd = get_drinks()
        elif self.path == '/people':
            jd = get_people()
        elif self.path == '/rounds':
            jd = get_rounds()
        elif self.path == '/rounds/open':
            jd = get_rounds(True)
        elif self.path == '/rounds/close':
            jd = get_rounds(False)

        self.wfile.write(jd.encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        data = json.loads(self.rfile.read(content_length))

        if self.path == '/drinks':
            post_drink(self, data)
        elif self.path == '/people':
            post_people(self, data)


if __name__ == "__main__":
    server_address = ('', 8081)
    httpd = HTTPServer(server_address, APIHandler)
    print("Starting server")
    httpd.serve_forever()

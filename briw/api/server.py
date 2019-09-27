
# from encoder import *
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from briw.persistence.drinks_controller import get_drinks_from_database, save_new_drink_in_database
from briw.persistence.people_controller import get_people_from_database, save_new_user_in_database
from briw.persistence.round_controller import get_rounds_from_database, create_new_open_round_in_database, close_round_in_database, add_order_to_round_in_database
from briw.classes.drink import Drink
from briw.classes.person import Person
from briw.classes.brew_round import Round
from briw.classes.order import Order
from briw.api.drink_encoder import DrinkEncoder
from briw.database.database_execption import DatabaseError
from briw.api.people_encoder import PeopleEncoder
from briw.api.round_encoder import RoundEncoder
from briw.data import texts


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
        print(texts.DATABASE_ERROR + texts.DRINK_NOT_ADDED)
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
        print(texts.DATABASE_ERROR + texts.ROUND_NOT_ADDED)
    finally:
        handler.end_headers()


def post_round(handler, data):
    try:
        brewer_person = Person(person_id=data['brewer_id'])
        new_round = Round(brewer=brewer_person)
        create_new_open_round_in_database(new_round)
        handler.send_response(201)
    except KeyError as e:
        print("JSON KEY ERRORS: "+str(e))
        handler.send_response(400)
    except DatabaseError:
        handler.send_response(500)
        print(texts.DATABASE_ERROR + texts.ROUND_NOT_ADDED)
    finally:
        handler.end_headers()


def post_close_round(handler, data):
    try:
        open_round = Round(round_id=data['round_id'])
        close_round_in_database(open_round)
        handler.send_response(201)
    except KeyError as e:
        print("JSON KEY ERRORS: "+str(e))
        handler.send_response(400)
    except DatabaseError:
        handler.send_response(500)
        print(texts.DATABASE_ERROR + texts.ROUND_NOT_ADDED)
    finally:
        handler.end_headers()


def post_add_order_to_round(handler, data):
    try:
        open_round = Round(round_id=data['round_id'])
        new_order = Order(Person(person_id=data['person_id']), Drink(
            drink_id=data['drink_id']))

        # TODO Check if the round is closed before to add the order
        add_order_to_round_in_database(open_round, new_order)

        handler.send_response(201)
    except KeyError as e:
        print("JSON KEY ERRORS: "+str(e))
        handler.send_response(400)
    except DatabaseError:
        handler.send_response(500)
        print(texts.DATABASE_ERROR + texts.ROUND_NOT_ADDED)
    finally:
        handler.end_headers()


def render_drinks(drinks):
    drinks_html = ""
    for drink in drinks:
        drinks_html += f'<li>{drink.name}</li>'
    return drinks_html


def render_people(people):
    people_html = ""
    for person in people:
        people_html += f'<li>{person.name}</li>'
    return people_html


def render_rounds(rounds):
    rounds_html = ""
    for _round in rounds:
        rounds_html += f'<li>{_round.get_string_date()} | maker -> {_round.brewer.name}</li>'
    return rounds_html


def render_website():
    drinks = get_drinks_from_database()
    people = get_people_from_database()
    rounds = get_rounds_from_database()

    return f"""
    <!doctype html>
    <html>
        <body>
            <p>Available drinks:</p>
            <ul>
                {render_drinks(drinks)}
            </ul>
            <p>People:</p>
            <ul>
                {render_people(people)}
            </ul>
            <p>Rounds:</p>
            <ul>
                {render_rounds(rounds)}
            </ul>
        </body>
    </html>
    """


class APIHandler(BaseHTTPRequestHandler):
    def _set_headers(self, content_type='text/json'):
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def do_GET(self):

        jd = None
        if self.path == '/':
            self._set_headers(content_type='text/html')
            jd = render_website()
        else:
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
        if jd:
            self.wfile.write(jd.encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        data = json.loads(self.rfile.read(content_length))
        if self.path == '/drinks':
            post_drink(self, data)
        elif self.path == '/people':
            post_people(self, data)
        elif self.path == '/rounds':
            post_round(self, data)
        elif self.path == '/rounds/close':
            post_close_round(self, data)
        elif self.path == '/rounds/order':
            post_add_order_to_round(self, data)


if __name__ == "__main__":
    server_address = ('', 8085)
    httpd = HTTPServer(server_address, APIHandler)
    print("Starting server")
    httpd.serve_forever()

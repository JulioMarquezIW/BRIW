
# from encoder import *
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from briw.persistence.drinks_controller import get_drinks_from_database, save_new_drink_in_database
from briw.persistence.people_controller import get_people_from_database, save_new_user_in_database
from briw.classes.drink import Drink
from briw.classes.person import Person
from briw.api.drink_encoder import DrinkEncoder
from briw.database.database_execption import DatabaseError
from briw.api.people_encoder import PeopleEncoder


class APIHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.end_headers()

    def do_GET(self):
        self._set_headers()

        if self.path == '/drinks':
            drinks = get_drinks_from_database()
            jd = json.dumps(drinks, cls=DrinkEncoder)
            self.wfile.write(jd.encode('utf-8'))
        elif self.path == '/people':
            people = get_people_from_database()
            jd = json.dumps(people, cls=PeopleEncoder)
            self.wfile.write(jd.encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        data = json.loads(self.rfile.read(content_length))

        if self.path == '/drinks':
            try:
                new_drink = Drink(data["name"])
                save_new_drink_in_database(new_drink)
                self.send_response(201)
            except KeyError as e:
                print("JSON KEY ERRORS: "+str(e))
                self.send_response(400)
            except DatabaseError:
                self.send_response(500)
                print('Database error, new drink will not be saved')
            finally:
                self.end_headers()
        elif self.path == '/people':
            try:
                new_person = Person(
                    data['name'], Drink('', data['favourite_drink_id']))

                save_new_user_in_database(new_person)
                self.send_response(201)
            except KeyError as e:
                print("JSON KEY ERRORS: "+str(e))
                self.send_response(400)
            except DatabaseError:
                self.send_response(500)
                print('Database error, new drink will not be saved')
            finally:
                self.end_headers()


if __name__ == "__main__":
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, APIHandler)
    print("Starting server")
    httpd.serve_forever()

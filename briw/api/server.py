
# from encoder import *
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from briw.persistence.drinks_controller import get_drinks_from_database
from briw.classes.person import Person
from briw.api.drink_encoder import DrinkEncoder


class PersonHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.end_headers()

    def do_GET(self):
        self._set_headers()

        drinks = get_drinks_from_database()
        jd = json.dumps(drinks, cls=DrinkEncoder)
        self.wfile.write(jd.encode('utf-8'))

    # def do_POST(self):
    #     content_length = int(self.headers['Content-Length'])
    #     data = json.loads(self.rfile.read(content_length),
    #                       object_hook=person_decoder)
    #     person = Person(data["name"])
    #     save_person(person)
    #     self.send_response(200)


if __name__ == "__main__":
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, PersonHandler)
    print("Starting server")
    httpd.serve_forever()

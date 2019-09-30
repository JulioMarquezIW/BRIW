from flask import Flask
from flask import json
from flask import url_for
import os
from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES
from flask import request
from flask import render_template
from briw.persistence.drinks_controller import get_drinks_from_database, save_new_drink_in_database, get_drink_by_id_from_database
from briw.persistence.round_controller import get_rounds_from_database, create_new_open_round_in_database, close_round_in_database, add_order_to_round_in_database
from briw.persistence.people_controller import get_people_from_database, save_new_user_in_database, get_person_by_id_from_database
from briw.classes.brew_round import Round
from briw.classes.order import Order
from briw.data import texts
from briw.classes.drink import Drink
from briw.classes.person import Person

template_dir = os.path.dirname(os.path.dirname(
    os.path.abspath(os.path.dirname(__file__))))
template_dir = os.path.join(template_dir, 'html')

print(template_dir)


app = Flask(__name__, template_folder=template_dir)


@app.route('/')
def hello_world():
    return jsonify(username='hola',
                   email='hola', )


@app.route('/api/rounds', methods=['GET', 'POST'])
def api_rounds():
    if request.method == 'GET':
        rounds = get_rounds_from_database()
        return {'rounds': [round.to_json() for round in rounds]}

    else:
        return "Unsupported HTTP Request Type"


@app.route('/api/rounds/open', methods=['GET'])
def api_open_rounds():
    if request.method == 'GET':
        rounds = get_rounds_from_database(True)
        return {'Open rounds': [round.to_json() for round in rounds]}

    else:
        return "Unsupported HTTP Request Type"


# TODO SACAR A OTRO ARCHIVO


def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response

# TODO SACAR A OTRO ARCHIVO


def bad_request(message):
    return error_response(400, message)


@app.route('/api/rounds/open/order', methods=['POST'])
def api_add_order_to_open_round():
    if request.method == 'POST':
        data = request.get_json() or {}
        open_rounds = get_rounds_from_database(True)

        if 'person_id' not in data or 'drink_id' not in data:
            return bad_request('must include person_id and drink_id fields')
        if len(open_rounds) == 0:
            return bad_request(texts.NOT_OPEN_ROUND)
        person = get_person_by_id_from_database(data['person_id'])
        if person == None:
            return bad_request('there is no user with that id')
        drink = get_drink_by_id_from_database(data['drink_id'])
        if drink == None:
            return bad_request('there is no drink with that id')

        new_order = Order(person, drink)

        # TODO Check if the round is closed before to add the order
        new_order = add_order_to_round_in_database(open_rounds[0], new_order)

        response = jsonify(new_order.to_json())
        response.status_code = 201

        return response

    else:
        return "Unsupported HTTP Request Type"


@app.route('/api/drinks', methods=['GET', 'POST'])
def api_get_drinks():
    if request.method == 'GET':
        drinks = get_drinks_from_database()
        return {'Drinks': [drink.to_json() for drink in drinks]}

    else:
        return "Unsupported HTTP Request Type"


@app.route('/api/drinks/<int:id>', methods=['GET', 'PUT'])
def api_get_drink_by_id(id):
    if request.method == 'GET':
        drink = get_drink_by_id_from_database(id)
        if drink == None:
            return bad_request('there is no drink with that id')
        return drink.to_json()
    else:
        return "Unsupported HTTP Request Type"


@app.route('/api/people/<int:id>', methods=['GET', 'PUT'])
def api_get_person_by_id(id):
    if request.method == 'GET':
        person = get_person_by_id_from_database(id)
        if person == None:
            return bad_request('there is no user with that id')
        return person.to_json()
    else:
        return "Unsupported HTTP Request Type"


@app.route('/api/people', methods=['GET', 'POST'])
def api_get_people():
    if request.method == 'GET':
        people = get_people_from_database()
        return {'People': [person.to_json() for person in people]}

    else:
        return "Unsupported HTTP Request Type"


@app.route('/drinks', methods=['GET', 'POST'])
def drinks():
    if request.method == 'GET':
        drinks = get_drinks_from_database()
        return render_template('drinks.html', title='Drinks', drinks=drinks)

    else:
        return "Unsupported HTTP Request Type"


@app.route('/form-example', methods=['GET', 'POST'])
def form_example():
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form['lastname']
        return render_template('myPostedPage.html', title='Posted', firstname=firstname, lastname=lastname)

    if request.method == 'GET':
        return render_template('myFormPage.html', title='Post')

    else:
        return "Unsupported HTTP Request Type"


if __name__ == '__main__':
    app.run()

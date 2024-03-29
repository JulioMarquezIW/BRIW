from flask import Flask, Response
from flask import json, redirect
from flask import url_for
import os
from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES
from flask import request
from flask import render_template
from briw.persistence.drinks_controller import get_drinks_from_database, save_new_drink_in_database, get_drink_by_id_from_database, search_drinks_by_name_from_database, delete_drink_in_database
from briw.persistence.round_controller import get_rounds_from_database, create_new_open_round_in_database, close_round_in_database, add_order_to_round_in_database, get_round_by_id
from briw.persistence.people_controller import get_people_from_database, save_new_user_in_database, get_person_by_id_from_database, search_person_by_name
from briw.classes.brew_round import Round
from briw.classes.order import Order
from briw.data import texts
from briw.classes.drink import Drink
from briw.classes.person import Person


template_dir = os.path.dirname(os.path.dirname(
    os.path.abspath(os.path.dirname(__file__))))
template_dir = os.path.join(template_dir, 'html')
static_dir = os.path.join(template_dir, 'static')

print(template_dir)


app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)


def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response


def bad_request(message):
    return error_response(400, message)
# ? API

# * ROUNDS


@app.route('/api/rounds/', methods=['GET', 'POST'])
def api_rounds():
    if request.method == 'GET':
        is_open = None
        if 'isOpen' in request.args:
            if request.args.get('isOpen').strip().upper() == 'TRUE':
                is_open = True
            elif request.args.get('isOpen').strip().upper() == 'FALSE':
                is_open = False

        rounds = get_rounds_from_database(is_open)
        return {'rounds': [round.to_json() for round in rounds]}

    if request.method == 'POST':
        data = request.get_json() or {}
        if 'brewer_name' not in data and 'brewer_id' not in data:
            return Response(status=400, response='must include brewer_name or brewer_id field')

        if 'brewer_name' in data and 'brewer_id' in data:
            return Response(status=400, response='must include only brewer_name or brewer_id field')
        if len(get_rounds_from_database(True)) > 0:
            return Response(status=400, response=texts.OPEN_ROUND_INFO)

        brewer = None
        if 'brewer_name' in data:
            people = search_person_by_name(data['brewer_name'])
            if len(people) == 0:
                return Response(status=400, response='there is no user with that name')
            if len(people) > 1:
                return Response(status=400, response='there is more than one user with that name')
            brewer = people[0]
        elif 'brewer_id' in data:
            brewer = get_person_by_id_from_database(data['brewer_id'])

        if brewer != None:
            new_round = Round(brewer=brewer)
            saved_round = create_new_open_round_in_database(new_round)

        response = jsonify(saved_round.to_json())
        response.status_code = 201

        return response

    else:
        return "Unsupported HTTP Request Type"


@app.route('/api/rounds/open', methods=['GET'])
def api_open_round():
    if request.method == 'GET':
        rounds = get_rounds_from_database(True)
        if len(rounds) > 1:
            app.logger.error('There is more than one open round. ')
        return rounds[-1].to_json()

    else:
        return "Unsupported HTTP Request Type"


@app.route('/api/rounds/open/order', methods=['POST'])
def api_add_order_to_open_round():
    if request.method == 'POST':
        data = request.get_json() or {}

        if 'person_id' not in data or 'drink_id' not in data:
            return Response(status=400, response='must include person_id and drink_id fields')
        open_rounds = get_rounds_from_database(True)
        if len(open_rounds) == 0:
            return Response(status=400, response=texts.NOT_OPEN_ROUND)
        person = get_person_by_id_from_database(data['person_id'])
        if person == None:
            return Response(status=400, response='there is no user with that id')
        drink = get_drink_by_id_from_database(data['drink_id'])
        if drink == None:
            return Response(status=400, response='there is no drink with that id')

        new_order = Order(person, drink)

        new_order = add_order_to_round_in_database(open_rounds[0], new_order)

        response = jsonify(new_order.to_json())
        response.status_code = 201

        return response

    else:
        return "Unsupported HTTP Request Type"


@app.route('/api/rounds/request', methods=['POST'])
def api_request_order_to_open_round():
    if request.method == 'POST':
        data = request.get_json() or {}

        if 'person_name' not in data:
            return bad_request('must include person_name field')
        open_rounds = get_rounds_from_database(True)
        if len(open_rounds) == 0:
            return bad_request(texts.NOT_OPEN_ROUND)

        people = search_person_by_name(data['person_name'])
        if len(people) == 0:
            return bad_request('there is no user with that name')
        if len(people) > 1:
            return bad_request('there is more than one user with that name')
        selected_person = people[0]
        selected_drink = selected_person.favourite_drink
        if 'drink' in data:
            drinks = search_drinks_by_name_from_database(data['drink'])
            if len(drinks) == 0:
                return bad_request('there is no drink with that name')
            if len(drinks) > 1:
                return bad_request('there is more than one drink with that name')
            selected_drink = drinks[0]

        new_order = Order(selected_person, selected_drink)

        new_order = add_order_to_round_in_database(open_rounds[0], new_order)

        response = jsonify(new_order.to_json())
        response.status_code = 201

        return response

    else:
        return "Unsupported HTTP Request Type"


@app.route('/api/rounds/open/close', methods=['POST'])
def api_close_open_round():
    if request.method == 'POST':

        open_rounds = get_rounds_from_database(True)
        if len(open_rounds) == 0:
            return Response(status=400, response=texts.NOT_OPEN_ROUND)

        open_round = open_rounds[0]
        close_round = close_round_in_database(open_round)

        response = jsonify(close_round.to_json())
        response.status_code = 201

        return response

    else:
        return "Unsupported HTTP Request Type"


@app.route('/api/rounds/<int:id>', methods=['GET', 'PUT'])
def api_get_round_by_id(id):
    if request.method == 'GET':
        getted_round = get_round_by_id(id)
        if getted_round == None:
            return Response(status=400, response='there is no round with that id')
        return getted_round.to_json()
    else:
        return "Unsupported HTTP Request Type"


# * DRINKS

@app.route('/api/drinks', methods=['GET', 'POST'])
def api_get_drinks():
    if request.method == 'GET':
        drinks = get_drinks_from_database()
        return {'Drinks': [drink.to_json() for drink in drinks]}

    if request.method == 'POST':
        data = request.get_json() or {}
        if 'name' not in data:
            return Response(status=400, response='must include name field')
        if len(search_drinks_by_name_from_database(data['name'])) > 0:
            return Response(status=400, response='there is already a drink with that name')

        new_drink = Drink(data['name'])
        save_drink = save_new_drink_in_database(new_drink)
        response = jsonify(save_drink.to_json())
        response.status_code = 201

        return response

    else:
        return "Unsupported HTTP Request Type"


@app.route('/api/drinks/<int:id>', methods=['GET', 'PUT'])
def api_get_drink_by_id(id):
    if request.method == 'GET':
        drink = get_drink_by_id_from_database(id)
        if drink == None:
            return Response(status=400, response='there is no drink with that id')
        return drink.to_json()

    else:
        return "Unsupported HTTP Request Type"


# * PEOPLE

@app.route('/api/people/<int:id>', methods=['GET', 'PUT'])
def api_get_person_by_id(id):
    if request.method == 'GET':
        person = get_person_by_id_from_database(id)
        if person == None:
            return Response(status=400, response='there is no user with that id')
        return person.to_json()
    else:
        return "Unsupported HTTP Request Type"


@app.route('/api/people', methods=['GET', 'POST'])
def api_get_people():
    if request.method == 'GET':
        people = get_people_from_database()
        return {'People': [person.to_json() for person in people]}

    if request.method == 'POST':
        data = request.get_json() or {}
        if 'name' not in data or 'favourite_drink_id' not in data:
            return Response(status=400, response='must include name and favourite_drink_id fields')
        drink = get_drink_by_id_from_database(data['favourite_drink_id'])
        if drink == None:
            return Response(status=400, response='there is no drink with that id')
        new_person = Person(data['name'], drink)
        save_person = save_new_user_in_database(new_person)
        response = jsonify(save_person.to_json())
        response.status_code = 201

        return response
    else:
        return "Unsupported HTTP Request Type"


# ? WEB SERVER

@app.route('/')
def hello_world():
    return render_template('index.html', title='BrIW')


@app.route('/drinks', methods=['GET', 'POST'])
def web_drinks():
    if request.method == 'GET':
        drinks = get_drinks_from_database()

        return render_template('drinks.html', title='Drinks', drinks=drinks)

    if request.method == 'POST':
        drink_name = request.form.get('drink_name')
        drinks = get_drinks_from_database()
        if len(drink_name) == 0:
            return render_template('drinks.html', title='Drinks', drinks=drinks, error_message='The name of the drink cannot be empty')
        if len(search_drinks_by_name_from_database(drink_name)) > 0:
            return render_template('drinks.html', title='Drinks', drinks=drinks, error_message='There is already a drink with that name')
        new_drink = Drink(drink_name)
        saved_drink = save_new_drink_in_database(new_drink)
        drinks.append(saved_drink)
        return render_template('drinks.html', title='Drinks', drinks=drinks)
    else:
        return "Unsupported HTTP Request Type"


@app.route('/people', methods=['GET', 'POST'])
def web_people():
    if request.method == 'GET':

        people = get_people_from_database()
        drinks = get_drinks_from_database()

        return render_template('people.html', title='People', people=people, drinks=drinks)

    if request.method == 'POST':
        drink_id = request.form.get('drink_id')

        drink = None
        if drink_id != 'None':
            drink = get_drink_by_id_from_database(drink_id)

        person_name = request.form.get('person_name').strip()
        people = get_people_from_database()
        drinks = get_drinks_from_database()

        if len(person_name) == 0:
            return render_template('people.html', title='People', people=people, drinks=drinks, error_message='The name of the person cannot be empty')
        if len(search_person_by_name(person_name)) > 0:
            return render_template('people.html', title='People', people=people, drinks=drinks, error_message='There is already a person with that name')

        new_person = Person(person_name, drink)
        saved_person = save_new_user_in_database(new_person)
        people.append(saved_person)

        return render_template('people.html', title='People', people=people, drinks=drinks)
    else:
        return "Unsupported HTTP Request Type"


@app.route('/rounds', methods=['GET'])
def web_rounds():
    if request.method == 'GET':

        rounds = get_rounds_from_database()

        return render_template('rounds.html', title='Rounds', rounds=rounds)

    else:
        return "Unsupported HTTP Request Type"


@app.route('/open-round', methods=['GET', 'POST'])
def web_open_round():
    if request.method == 'GET':

        rounds = get_rounds_from_database(True)
        people = get_people_from_database()
        drinks = []

        open_round = None
        if len(rounds) > 0:
            open_round = rounds[-1]
            drinks = get_drinks_from_database()

        return render_template('open_round.html', title='Open Round', open_round=open_round, people=people, drinks=drinks)

    if request.method == 'POST':

        person_id = request.form.get('person_id')

        person = get_person_by_id_from_database(person_id)
        new_round = Round(brewer=person)
        create_new_open_round_in_database(new_round)

        return redirect(url_for('web_open_round'))

    else:
        return "Unsupported HTTP Request Type"


@app.route('/add-order', methods=['POST'])
def web_add_order():
    if request.method == 'POST':
        round_id = request.form.get('round_id')
        drink_id = request.form.get('drink_id')
        person_id = request.form.get('person_id')

        open_round = get_round_by_id(round_id)

        person = get_person_by_id_from_database(person_id)
        drink = get_drink_by_id_from_database(drink_id)

        new_order = Order(person, drink)

        add_order_to_round_in_database(open_round, new_order)

        return redirect(url_for('web_open_round'))

    else:
        return "Unsupported HTTP Request Type"


@app.route('/close-round', methods=['POST'])
def web_close_round():
    if request.method == 'POST':
        round_id = request.form.get('round_id')

        close_round_in_database(Round(round_id=round_id))

        return redirect(url_for('web_rounds'))

    else:
        return "Unsupported HTTP Request Type"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8085)

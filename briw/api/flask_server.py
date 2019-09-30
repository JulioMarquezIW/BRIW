from flask import Flask
from flask import json
import os
from flask import jsonify
from flask import request
from flask import render_template
from briw.persistence.drinks_controller import get_drinks_from_database, save_new_drink_in_database
from briw.persistence.round_controller import get_rounds_from_database, create_new_open_round_in_database, close_round_in_database, add_order_to_round_in_database


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

from flask import Flask
import os
from flask import request
from flask import render_template
from briw.persistence.drinks_controller import get_drinks_from_database, save_new_drink_in_database


template_dir = os.path.dirname(os.path.dirname(
    os.path.abspath(os.path.dirname(__file__))))
template_dir = os.path.join(template_dir, 'html')

print(template_dir)


app = Flask(__name__, template_folder=template_dir)


@app.route('/')
def hello_world():
    return 'Hello World!'


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

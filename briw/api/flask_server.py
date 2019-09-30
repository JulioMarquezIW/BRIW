from flask import Flask
import os


template_dir = os.path.dirname(os.path.dirname(
    os.path.abspath(os.path.dirname(__file__))))
template_dir = os.path.join(template_dir, 'html')

print(template_dir)


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()

from flask import Flask
from flask_restplus import Api
from flask import render_template

from src.controller.status_controller import api as status_ns
from src.controller.addition_controller import api as add_ns
from src.controller.multiplication_controller import api as multi_ns

app_title = 'Template project for Flask'
app_description = 'Showcase project for building Flask micro-service web app.'

app = Flask(__name__)

api = Api(app=app, title=app_title,
          version='1.0',
          description=app_description)

api.add_namespace(status_ns, path="/status")
api.add_namespace(add_ns, path="/api/addition")
api.add_namespace(multi_ns, path="/api/multiplication")


@app.route('/home/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

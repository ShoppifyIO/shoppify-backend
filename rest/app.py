from flask import Flask
from flask_cors import CORS
from rest.blueprints.user import user_blueprint


def create_app() -> Flask:
    app = Flask(__name__)
    app.config['LIVESERVER_PORT'] = 5000
    app.config['SECRET_KEY'] = '1234567890'

    CORS(app)

    app.register_blueprint(user_blueprint, url_prefix='')

    return app

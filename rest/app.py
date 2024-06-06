from flask import Flask
from flask_cors import CORS

from rest.blueprints.shopping_list import shopping_list_blueprint
from rest.blueprints.user import user_blueprint
from rest.blueprints.category import category_blueprint
from rest.blueprints.friend import friend_blueprint


def create_app() -> Flask:
    app = Flask(__name__)
    app.config['LIVESERVER_PORT'] = 5000
    app.config['SECRET_KEY'] = '1234567890'

    CORS(app)

    app.register_blueprint(user_blueprint, url_prefix='')
    app.register_blueprint(shopping_list_blueprint, url_prefix='/shopping-list')
    app.register_blueprint(category_blueprint, url_prefix='/categories')
    app.register_blueprint(friend_blueprint, url_prefix='/friends')

    return app

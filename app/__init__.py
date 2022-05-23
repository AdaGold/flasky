from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_cors import CORS
import os

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()


def create_app(test_config=None):
    # __name__ store the name of the module we're in
    app = Flask(__name__)
    CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if test_config is None:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DEV_DB')
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('TEST_DB')

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes.dog_routes import dog_bp
    app.register_blueprint(dog_bp)

    from .routes.cat_routes import cat_bp
    app.register_blueprint(cat_bp)

    from app.models.dog import Dog

    return app
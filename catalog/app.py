from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config='catalog.config.ProductionConfig'):
    # Create app
    app = Flask(__name__)
    app.config.from_object(config)

    # Initialize extensions
    db.init_app(app)

    return app

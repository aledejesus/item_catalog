from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app(config='catalog.config.ProductionConfig'):
    """
    Create flask app instance and initialize all extensions

    Arguments:
        - config (string): path to object to be used to
            configure app

    Returns:
        - flask.Flask instance
    """
    # Create app
    app = Flask(__name__)
    app.config.from_object(config)

    # Register blueprints
    reg_bps(app)

    # Import models (for migration purposes)
    from . import Category, Item, AppUser  # noqa: F401

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    return app


def reg_bps(app):
    """
    Register blueprints to app

    Arguments:
        - app (flask.Flask): app instance to
            register blueprints to

    Returns:
        None
    """
    from . import categories_bp, items_bp, users_bp

    app.register_blueprint(categories_bp, url_prefix='/categories')
    app.register_blueprint(items_bp, url_prefix='/items')
    app.register_blueprint(users_bp)

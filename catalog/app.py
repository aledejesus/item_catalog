from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config='catalog.config.ProductionConfig'):
    # Create app
    app = Flask(__name__)
    app.config.from_object(config)

    # Register blueprints
    reg_bps(app)

    # Initialize extensions
    db.init_app(app)

    return app


def reg_bps(app):
    from catalog.categories.views import categories_bp
    from catalog.home.views import home_bp

    app.register_blueprint(categories_bp, url_prefix='/categories')
    app.register_blueprint(home_bp)

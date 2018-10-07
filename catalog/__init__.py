"""
Import all objects and classes app.py needs to run
flask app and all objects the app needs to function
properly (e.g., db and cache objects).
"""

from .app import create_app, db  # noqa: F401

# Import models
from catalog.categories.models import Category  # noqa: F401
from catalog.items.models import Item  # noqa: F401
from catalog.users.models import AppUser  # noqa:F401

# Import blueprints
from catalog.categories.views import categories_bp  # noqa: F401
from catalog.items.views import items_bp  # noqa: F401
from catalog.users.views import users_bp  # noqa: F401

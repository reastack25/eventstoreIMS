# routes.py

from flask import Blueprint
from api.inventory.routes import inventory_bp
from api.categories.routes import category_bp
from api.inventory.routes import inventory_bp
from api.categories.routes import category_bp
from api.reports.routes import reports_bp
api = Blueprint("api",__name__)

@api.route("/")
def health_check():
    return {
        "message": "EventStore IMS Running"
    }

def register_routes(app):
    app.register_blueprint(api)

def register_routes(app):
    app.register_blueprint(category_bp)

def register_routes(app):
    app.register_blueprint(category_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(reports_bp)
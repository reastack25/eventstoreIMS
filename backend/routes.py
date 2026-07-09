# routes.py

from flask import Blueprint
from api.auth.routes import auth_bp
from api.categories.routes import category_bp
from api.inventory.routes import inventory_bp
# from api.inventory_transactions.routes import inventory_tx_bp
from api.reports.routes import reports_bp

api = Blueprint("api", __name__)

@api.route("/")
def health_check():
    return {"message": "EventStore IMS Running"}

def register_routes(app):
    app.register_blueprint(api)
    app.register_blueprint(auth_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(inventory_bp)
    # app.register_blueprint(inventory_tx_bp)
    app.register_blueprint(reports_bp)
# routes.py

from flask import Blueprint

api = Blueprint("api",__name__)

@api.route("/")
def health_check():
    return {
        "message": "EventStore IMS Running"
    }

def register_routes(app):
    app.register_blueprint(api)
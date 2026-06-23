from flask import Flask
from extensions import (db,jwt,migrate,cors)
from models.category import Category
from models.item import Item

def create_app():
    app = Flask(__name__)
    app.config.from_object(
        "config.development.DevelopmentConfig"
    )

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

    from routes import register_routes
    register_routes(app)

    return app
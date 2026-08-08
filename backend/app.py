import os
from flask import Flask
from extensions import db, jwt, migrate, cors
from models.category import Category
from models.item import Item
from middleware.error_handler import register_error_handlers

def create_app():
    app = Flask(__name__)

    env = os.getenv("FLASK_ENV", "development")

    if env == "production":
        app.config.from_object("config.production.ProductionConfig")
    elif env == "testing":
        app.config.from_object("config.testing.TestingConfig")
    else:
        app.config.from_object("config.development.DevelopmentConfig")

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    register_error_handlers(app)

    from models.user import User
    from models.audit_log import AuditLog
    from models.damage_log import DamageLog
    from models.inventory_transaction import InventoryTransaction
    from models.event import Event
    from models.job_card import JobCard
    from models.job_card_item import JobCardItem
    from routes import register_routes
    register_routes(app)

    return app

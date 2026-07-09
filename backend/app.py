from flask import Flask
from extensions import (db,jwt,migrate,cors)
from models.category import Category
from models.item import Item

from middleware.error_handler import (register_error_handlers)
# from middleware.logging_middleware import configure_logging

def create_app():
    app = Flask(__name__)
    app.config.from_object(
        "config.development.DevelopmentConfig"
    )

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    register_error_handlers(app)
    # configure_logging()
    # api_docs.init_app(app)
    
    # from utils.logger import configure_logging
           
    from models.user import User
    from models.audit_log import AuditLog
    from models.damage_log import DamageLog
    from models.inventory_transaction import InventoryTransaction
    from routes import register_routes
    register_routes(app)

    return app
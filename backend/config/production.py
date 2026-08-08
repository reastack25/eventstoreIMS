import os
from config.base import BaseConfig

class ProductionConfig(BaseConfig):
    DEBUG = False

    # Fix Railway postgres:// -> postgresql://
    db_url = os.getenv("DATABASE_URL", "")
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = db_url

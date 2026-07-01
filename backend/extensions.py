from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from flask_smorest import Api

api_docs = Api()
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
cors = CORS()


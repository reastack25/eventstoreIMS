from config.base import BaseConfig

class TestingConfig(BaseConfig):

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    
    API_TITLE          = "EventStore IMS API"
    API_VERSION        = "v1"
    OPENAPI_VERSION    = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/docs"
    OPENAPI_SWAGGER_UI_URL  = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
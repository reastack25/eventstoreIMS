from config.base import BaseConfig

class ProductionConfig(BaseConfig):

    DEBUG = False

    API_TITLE          = "EventStore IMS API"
    API_VERSION        = "v1"
    OPENAPI_VERSION    = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    
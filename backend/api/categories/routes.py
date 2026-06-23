from flask import Blueprint
from flask import jsonify
from flask import request

from services.category_service import CategoryService
from schemas.category_schema import CategorySchema

category_bp = Blueprint("categories",__name__,url_prefix="/api/categories")

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)
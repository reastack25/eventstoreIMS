from flask import Blueprint
from flask import jsonify
from flask import request

from services.category_service import CategoryService
from schemas.category_schema import CategorySchema

category_bp = Blueprint("categories",__name__,url_prefix="/api/categories")

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)

@category_bp.route("/", methods=["POST"])
def create_category():

    data = request.get_json()
    category = CategoryService.create_category(data)

    return (
        category_schema.dump(category),201
    )
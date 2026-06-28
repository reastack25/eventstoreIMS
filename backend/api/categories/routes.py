from flask import Blueprint
from flask import jsonify
from flask import request

from services.category_service import CategoryService
from schemas.category_schema import CategorySchema

category_bp = Blueprint("categories",__name__,url_prefix="/api/v1/categories")

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)

@category_bp.route("/", methods=["POST"])
def create_category():

    data = request.get_json()
    category = CategoryService.create_category(data)

    return (
        category_schema.dump(category),201
    )

@category_bp.route("/", methods=["GET"])
def get_categories():

    categories = CategoryService.get_categories()

    return jsonify(
        categories_schema.dump(categories)
    )
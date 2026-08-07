from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from middleware.role_middleware import permission_required
from models.category import Category
from extensions import db

category_bp = Blueprint("categories", __name__, url_prefix="/api/v1/categories")

@category_bp.route("/", methods=["GET"])
@jwt_required()
def get_categories():
    cats = Category.query.order_by(Category.name).all()
    return jsonify([{"id": c.id, "name": c.name, "description": c.description} for c in cats]), 200

@category_bp.route("/", methods=["POST"])
@jwt_required()
@permission_required("manage_categories")
def create_category():
    data = request.get_json()
    if not data.get("name"):
        return jsonify({"error": "name is required"}), 422

    cat = Category(name=data["name"], description=data.get("description", ""))
    db.session.add(cat)
    db.session.commit()
    return jsonify({"id": cat.id, "name": cat.name, "description": cat.description}), 201

@category_bp.route("/<int:cat_id>", methods=["PUT"])
@jwt_required()
@permission_required("manage_categories")
def update_category(cat_id):
    cat  = Category.query.get_or_404(cat_id)
    data = request.get_json()
    if data.get("name"):
        cat.name = data["name"]
    if data.get("description") is not None:
        cat.description = data["description"]
    db.session.commit()
    return jsonify({"id": cat.id, "name": cat.name, "description": cat.description}), 200

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from middleware.role_middleware import permission_required
from services.inventory_service import InventoryService
from repositories.inventory_repo import ItemRepository

inventory_bp = Blueprint("inventory", __name__, url_prefix="/api/v1/inventory")

@inventory_bp.route("/", methods=["GET"])
@jwt_required()
def get_inventory():
    page     = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    search   = request.args.get("search", None, type=str)
    per_page = min(per_page, 100)

    pagination = ItemRepository.get_all_paginated(page, per_page, search)

    return jsonify({
        "items": [item.to_dict() for item in pagination.items],
        "meta": {
            "page":        pagination.page,
            "per_page":    pagination.per_page,
            "total_items": pagination.total,
            "total_pages": pagination.pages,
            "has_next":    pagination.has_next,
            "has_prev":    pagination.has_prev,
            "search":      search
        }
    }), 200


@inventory_bp.route("/receive", methods=["POST"])
@jwt_required()
@permission_required("receive_stock")
def receive():
    data         = request.get_json()
    performed_by = get_jwt_identity()

    if not data.get("item_id") or not data.get("quantity"):
        return jsonify({"error": "item_id and quantity are required"}), 422
    if data["quantity"] <= 0:
        return jsonify({"error": "Quantity must be greater than zero"}), 422

    item = InventoryService.receive_stock(data, performed_by)
    return jsonify({"message": "Stock received successfully", "item": item.to_dict()}), 200


@inventory_bp.route("/dispatch", methods=["POST"])
@jwt_required()
@permission_required("dispatch_stock")
def dispatch():
    data         = request.get_json()
    performed_by = get_jwt_identity()

    if not data.get("item_id") or not data.get("quantity"):
        return jsonify({"error": "item_id and quantity are required"}), 422
    if data["quantity"] <= 0:
        return jsonify({"error": "Quantity must be greater than zero"}), 422

    try:
        item = InventoryService.dispatch_stock(data, performed_by)
    except ValueError as e:
        return jsonify({"error": str(e)}), 409

    return jsonify({"message": "Stock dispatched successfully", "item": item.to_dict()}), 200


@inventory_bp.route("/return", methods=["POST"])
@jwt_required()
@permission_required("return_stock")
def return_stock():
    data         = request.get_json()
    performed_by = get_jwt_identity()

    if not data.get("item_id") or not data.get("quantity"):
        return jsonify({"error": "item_id and quantity are required"}), 422
    if data["quantity"] <= 0:
        return jsonify({"error": "Quantity must be greater than zero"}), 422

    item = InventoryService.return_stock(data, performed_by)
    return jsonify({"message": "Stock returned successfully", "item": item.to_dict()}), 200


@inventory_bp.route("/damage", methods=["POST"])
@jwt_required()
@permission_required("report_damage")
def damage():
    data         = request.get_json()
    performed_by = get_jwt_identity()

    if not data.get("item_id") or not data.get("quantity"):
        return jsonify({"error": "item_id and quantity are required"}), 422
    if data["quantity"] <= 0:
        return jsonify({"error": "Quantity must be greater than zero"}), 422

    try:
        item = InventoryService.report_damage(data, performed_by)
    except ValueError as e:
        return jsonify({"error": str(e)}), 409

    return jsonify({"message": "Damage reported successfully", "item": item.to_dict()}), 200

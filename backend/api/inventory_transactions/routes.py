from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from middleware.role_middleware import permission_required
from services.inventory_service import InventoryService

inventory_tx_bp = Blueprint(
    "inventory_transactions",
    __name__,
    url_prefix="/api/v1/inventory"
)

@inventory_tx_bp.route("/receive", methods=["POST"])
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


@inventory_tx_bp.route("/dispatch", methods=["POST"])
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


@inventory_tx_bp.route("/return", methods=["POST"])
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


@inventory_tx_bp.route("/damage", methods=["POST"])
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

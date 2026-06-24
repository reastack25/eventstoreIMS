from flask import Blueprint
from flask import jsonify
from flask import request

from services.inventory_service import InventoryService
from schemas.inventory_schema import ItemSchema

inventory_bp = Blueprint("inventory", __name__,url_prefix="/api/inventory")

item_schema = ItemSchema()
items_schema = ItemSchema(many=True)

# @inventory_bp.route("//")
# def health():
#     return {
#         "module": "inventory",
#         "status": "running"
#     }

@inventory_bp.route("/", methods=["POST"])
def create_item():

    data = request.get_json()
    item = InventoryService.create_item(data)
    return (
        item_schema.dump(item),201
    )

@inventory_bp.route("/", methods=["GET"])
def get_items():

    items = InventoryService.get_items()
    return jsonify(
        items_schema.dump(items)
    )
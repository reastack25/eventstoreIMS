from flask import Blueprint

inventory_bp = Blueprint("inventory", __name__,url_prefix="/api/inventory")

@inventory_bp.route("/")
def health():
    return {
        "module": "inventory",
        "status": "running"
    }
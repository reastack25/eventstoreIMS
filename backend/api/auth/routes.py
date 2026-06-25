from flask import Blueprint
from flask_jwt_extended import (create_access_token)

auth_bp = Blueprint("auth",__name__,url_prefix="/api/auth")

@auth_bp.route("/register",methods=["POST"])
def register():
    data = request.get_json()
    user = AuthService.register(data)
    return {
        "message": "User created"
    }, 201
# api/auth/routes.py

from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from services.auth_service import AuthService
from schemas.auth_schema import RegisterSchema,LoginSchema
from repositories.user_repo import UserRepository

auth_bp = Blueprint("auth",__name__,url_prefix="/api/v1/auth"
)

register_schema = RegisterSchema()

@auth_bp.route("/register", methods=["POST"])
def register():

     data = request.get_json()
    try:
        validated_data = register_schema.load(data)
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 422

    existing = UserRepository.get_by_email(validated_data["email"])
    if existing:
        return jsonify({"error": "Email already registered"}), 409

  
    user = AuthService.register(validated_data)
       return jsonify({
        "message": "User created successfully",
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "role": user.role
        }
    }), 201

@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()
    try:
        validated_data = login_schema.load(data)
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 422

    token, result = AuthService.login(validated_data)

    if token is None and isinstance(result, str):
        return jsonify({"error": result}), 403

    if token is None:
        return jsonify({"error": "Invalid email or password"}), 401
   
    return jsonify({
        "message": "Login successful",
        "access_token": token,
        "user": {
            "id": result.id,
            "full_name": result.full_name,
            "email": result.email,
            "role": result.role
        }
    }), 200

from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from utils.roles import ROLE_PERMISSIONS

def role_required(*allowed_roles):
    """
    Restrict endpoint to specific roles.
    Usage: @role_required("ADMIN", "STORE_MANAGER")
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user_role = claims.get("role")

            if user_role not in allowed_roles:
                return jsonify({
                    "error":   "Access denied",
                    "message": f"Required roles: {', '.join(allowed_roles)}"
                }), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator


def permission_required(permission):
    """
    Restrict endpoint by permission string.
    Usage: @permission_required("receive_stock")
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims    = get_jwt()
            user_role = claims.get("role")

            allowed = ROLE_PERMISSIONS.get(user_role, [])

            if permission not in allowed:
                return jsonify({
                    "error":   "Access denied",
                    "message": f"You do not have permission to perform this action"
                }), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator
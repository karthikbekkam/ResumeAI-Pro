from functools import wraps
from flask import session, redirect, url_for, flash, request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from models.user import User

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check session auth first (for Jinja template pages)
        if "user_id" in session:
            return f(*args, **kwargs)
        
        # Check JWT auth (for API calls)
        try:
            verify_jwt_in_request(optional=True)
            user_id = get_jwt_identity()
            if user_id:
                session["user_id"] = int(user_id) if isinstance(user_id, str) else user_id
                return f(*args, **kwargs)
        except Exception:
            pass

        if request.is_json or request.path.startswith("/api/"):
            return jsonify({"error": "Unauthorized access. Please login."}), 401
        
        flash("Please log in to access this page.", "warning")
        return redirect(url_for("auth.login", next=request.path))
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get("user_id")
        user_role = session.get("user_role")

        if not user_id:
            try:
                verify_jwt_in_request(optional=True)
                jwt_uid = get_jwt_identity()
                if jwt_uid:
                    user = User.query.get(int(jwt_uid))
                    if user:
                        user_id = user.id
                        user_role = user.role
            except Exception:
                pass

        if not user_id or user_role != "admin":
            if request.is_json or request.path.startswith("/api/"):
                return jsonify({"error": "Forbidden. Admin privileges required."}), 403
            
            flash("Admin privileges are required to access this page.", "danger")
            return redirect(url_for("main.index"))
        
        return f(*args, **kwargs)
    return decorated_function

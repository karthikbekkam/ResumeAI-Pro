from flask_jwt_extended import create_access_token
from extensions import db
from models.user import User
from models.activity import ActivityLog
from utils.helpers import validate_email

class AuthService:
    @staticmethod
    def register_user(email, password, full_name, role="user", target_role=None, bio=None):
        if not email or not password or not full_name:
            return {"error": "Email, password, and full name are required."}, 400

        if not validate_email(email):
            return {"error": "Invalid email address format."}, 400

        if len(password) < 6:
            return {"error": "Password must be at least 6 characters long."}, 400

        existing_user = User.query.filter_by(email=email.lower().strip()).first()
        if existing_user:
            return {"error": "An account with this email already exists."}, 409

        new_user = User(
            email=email.lower().strip(),
            full_name=full_name.strip(),
            role=role if role in ["user", "admin"] else "user",
            target_role=target_role.strip() if target_role else None,
            bio=bio.strip() if bio else None
        )
        new_user.set_password(password)

        try:
            db.session.add(new_user)
            db.session.commit()

            AuthService.log_activity(new_user.id, "REGISTER", "User registered successfully.")
            access_token = create_access_token(identity=str(new_user.id))

            return {
                "message": "User registered successfully.",
                "user": new_user.to_dict(),
                "access_token": access_token
            }, 201
        except Exception as e:
            db.session.rollback()
            return {"error": f"Database error during registration: {str(e)}"}, 500

    @staticmethod
    def authenticate_user(email, password):
        if not email or not password:
            return {"error": "Email and password are required."}, 400

        user = User.query.filter_by(email=email.lower().strip()).first()
        if not user or not user.check_password(password):
            return {"error": "Invalid email or password credentials."}, 401

        access_token = create_access_token(identity=str(user.id))
        AuthService.log_activity(user.id, "LOGIN", "User logged in.")

        return {
            "message": "Login successful.",
            "user": user.to_dict(),
            "access_token": access_token
        }, 200

    @staticmethod
    def log_activity(user_id, action, description=None, ip_address=None):
        try:
            log = ActivityLog(
                user_id=user_id,
                action=action,
                description=description,
                ip_address=ip_address
            )
            db.session.add(log)
            db.session.commit()
        except Exception:
            db.session.rollback()

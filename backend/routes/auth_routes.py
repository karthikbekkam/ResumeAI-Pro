from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from services.auth_service import AuthService
from models.user import User
from models.resume import Resume
from extensions import db
from utils.decorators import login_required

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
            email = data.get("email")
            password = data.get("password")
            full_name = data.get("full_name")
            target_role = data.get("target_role")
            role = data.get("role", "user")
        else:
            email = request.form.get("email")
            password = request.form.get("password")
            full_name = request.form.get("full_name")
            target_role = request.form.get("target_role")
            role = request.form.get("role", "user")

        result, status_code = AuthService.register_user(
            email=email,
            password=password,
            full_name=full_name,
            role=role,
            target_role=target_role
        )

        if status_code == 201:
            user_data = result["user"]
            session["user_id"] = user_data["id"]
            session["user_name"] = user_data["full_name"]
            session["user_email"] = user_data["email"]
            session["user_role"] = user_data["role"]

            if request.is_json:
                return jsonify(result), 201

            flash("Account registered successfully! Welcome to ResumeAI Pro.", "success")
            return redirect(url_for("dashboard.user_dashboard"))
        else:
            if request.is_json:
                return jsonify(result), status_code
            flash(result.get("error", "Registration failed."), "danger")

    return render_template("auth/register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
            email = data.get("email")
            password = data.get("password")
        else:
            email = request.form.get("email")
            password = request.form.get("password")

        result, status_code = AuthService.authenticate_user(email, password)

        if status_code == 200:
            user_data = result["user"]
            session["user_id"] = user_data["id"]
            session["user_name"] = user_data["full_name"]
            session["user_email"] = user_data["email"]
            session["user_role"] = user_data["role"]

            if request.is_json:
                return jsonify(result), 200

            flash(f"Welcome back, {user_data['full_name']}!", "success")
            next_page = request.args.get("next")
            if next_page:
                return redirect(next_page)
            
            if user_data["role"] == "admin":
                return redirect(url_for("admin.admin_dashboard"))
            return redirect(url_for("dashboard.user_dashboard"))
        else:
            if request.is_json:
                return jsonify(result), status_code
            flash(result.get("error", "Invalid login credentials."), "danger")

    return render_template("auth/login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out safely.", "info")
    return redirect(url_for("main.index"))

@auth_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user = User.query.get(session["user_id"])
    if not user:
        session.clear()
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        action = request.form.get("action")

        if action == "update_profile":
            user.full_name = request.form.get("full_name", user.full_name).strip()
            user.target_role = request.form.get("target_role", user.target_role).strip()
            user.bio = request.form.get("bio", user.bio).strip()
            
            db.session.commit()
            session["user_name"] = user.full_name
            AuthService.log_activity(user.id, "UPDATE_PROFILE", "Updated profile details.")
            flash("Profile details updated successfully!", "success")

        elif action == "change_password":
            current_password = request.form.get("current_password")
            new_password = request.form.get("new_password")
            confirm_password = request.form.get("confirm_password")

            if not user.check_password(current_password):
                flash("Current password entered is incorrect.", "danger")
            elif len(new_password) < 6:
                flash("New password must be at least 6 characters long.", "warning")
            elif new_password != confirm_password:
                flash("New password and confirmation do not match.", "danger")
            else:
                user.set_password(new_password)
                db.session.commit()
                AuthService.log_activity(user.id, "CHANGE_PASSWORD", "Password changed.")
                flash("Password updated successfully!", "success")

        elif action == "delete_account":
            db.session.delete(user)
            db.session.commit()
            session.clear()
            flash("Your account has been deleted permanently.", "info")
            return redirect(url_for("main.index"))

    resumes = Resume.query.filter_by(user_id=user.id).order_by(Resume.upload_date.desc()).all()
    return render_template("auth/profile.html", user=user, resumes=resumes)

# REST API Profile Endpoints
@auth_bp.route("/api/me", methods=["GET"])
@login_required
def api_me():
    user = User.query.get(session["user_id"])
    return jsonify(user.to_dict()), 200

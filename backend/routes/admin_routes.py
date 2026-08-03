import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from extensions import db
from models.user import User
from models.resume import Resume
from models.ats_report import ATSReport
from models.job_match import JobMatch
from models.interview import InterviewPrep
from models.activity import ActivityLog
from utils.helpers import format_file_size
from utils.decorators import admin_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/dashboard")
@admin_required
def admin_dashboard():
    total_users = User.query.count()
    total_resumes = Resume.query.count()
    total_job_matches = JobMatch.query.count()
    total_interview_preps = InterviewPrep.query.count()

    all_resumes = Resume.query.all()
    avg_ats = round(sum(r.ats_score for r in all_resumes) / total_resumes, 1) if total_resumes > 0 else 0.0

    stats = {
        "total_users": total_users,
        "total_resumes": total_resumes,
        "total_job_matches": total_job_matches,
        "total_interview_preps": total_interview_preps,
        "avg_system_ats": avg_ats
    }

    recent_users = User.query.order_by(User.created_at.desc()).limit(6).all()
    recent_resumes = Resume.query.order_by(Resume.upload_date.desc()).limit(6).all()
    recent_activities = ActivityLog.query.order_by(ActivityLog.created_at.desc()).limit(8).all()

    return render_template(
        "admin/admin_dashboard.html",
        stats=stats,
        recent_users=recent_users,
        recent_resumes=recent_resumes,
        recent_activities=recent_activities,
        format_file_size=format_file_size
    )

@admin_bp.route("/users")
@admin_required
def users():
    search_query = request.args.get("search", "").strip()
    page = request.args.get("page", 1, type=int)
    
    query = User.query
    if search_query:
        query = query.filter((User.full_name.ilike(f"%{search_query}%")) | (User.email.ilike(f"%{search_query}%")))
    
    pagination = query.order_by(User.created_at.desc()).paginate(page=page, per_page=10, error_out=False)
    
    if request.is_json:
        return jsonify({
            "users": [u.to_dict() for u in pagination.items],
            "total": pagination.total,
            "pages": pagination.pages,
            "current_page": page
        }), 200

    return render_template("admin/users.html", pagination=pagination, search_query=search_query)

@admin_bp.route("/users/delete/<int:user_id>", methods=["POST"])
@admin_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        if request.is_json:
            return jsonify({"error": "User not found."}), 404
        flash("User not found.", "warning")
        return redirect(url_for("admin.users"))

    if user.id == session.get("user_id"):
        if request.is_json:
            return jsonify({"error": "You cannot delete your own admin account while logged in."}), 400
        flash("You cannot delete your own active admin account.", "danger")
        return redirect(url_for("admin.users"))

    try:
        # Cleanup resume files
        user_resumes = Resume.query.filter_by(user_id=user.id).all()
        for r in user_resumes:
            if os.path.exists(r.file_path):
                os.remove(r.file_path)

        db.session.delete(user)
        db.session.commit()

        if request.is_json:
            return jsonify({"message": f"User {user.full_name} deleted successfully."}), 200

        flash(f"User '{user.full_name}' deleted successfully.", "info")
        return redirect(url_for("admin.users"))
    except Exception as e:
        db.session.rollback()
        if request.is_json:
            return jsonify({"error": str(e)}), 500
        flash(f"Error deleting user: {str(e)}", "danger")
        return redirect(url_for("admin.users"))

@admin_bp.route("/resumes")
@admin_required
def resumes():
    search_query = request.args.get("search", "").strip()
    page = request.args.get("page", 1, type=int)

    query = Resume.query
    if search_query:
        query = query.filter(Resume.original_filename.ilike(f"%{search_query}%"))

    pagination = query.order_by(Resume.upload_date.desc()).paginate(page=page, per_page=10, error_out=False)

    if request.is_json:
        return jsonify({
            "resumes": [r.to_dict() for r in pagination.items],
            "total": pagination.total,
            "pages": pagination.pages,
            "current_page": page
        }), 200

    return render_template("admin/resumes.html", pagination=pagination, search_query=search_query, format_file_size=format_file_size)

@admin_bp.route("/resumes/delete/<int:resume_id>", methods=["POST"])
@admin_required
def delete_resume(resume_id):
    resume = Resume.query.get(resume_id)
    if not resume:
        if request.is_json:
            return jsonify({"error": "Resume not found."}), 404
        flash("Resume not found.", "warning")
        return redirect(url_for("admin.resumes"))

    try:
        if os.path.exists(resume.file_path):
            os.remove(resume.file_path)

        db.session.delete(resume)
        db.session.commit()

        if request.is_json:
            return jsonify({"message": "Resume deleted successfully."}), 200

        flash("Resume deleted by admin.", "info")
        return redirect(url_for("admin.resumes"))
    except Exception as e:
        db.session.rollback()
        if request.is_json:
            return jsonify({"error": str(e)}), 500
        flash(f"Error deleting resume: {str(e)}", "danger")
        return redirect(url_for("admin.resumes"))

@admin_bp.route("/api/analytics")
@admin_required
def analytics_api():
    total_users = User.query.count()
    total_resumes = Resume.query.count()
    total_job_matches = JobMatch.query.count()
    total_interview_preps = InterviewPrep.query.count()

    # Distribution of ATS Scores
    score_ranges = {"0-40": 0, "41-60": 0, "61-80": 0, "81-100": 0}
    resumes = Resume.query.all()
    for r in resumes:
        if r.ats_score <= 40:
            score_ranges["0-40"] += 1
        elif r.ats_score <= 60:
            score_ranges["41-60"] += 1
        elif r.ats_score <= 80:
            score_ranges["61-80"] += 1
        else:
            score_ranges["81-100"] += 1

    return jsonify({
        "totals": {
            "users": total_users,
            "resumes": total_resumes,
            "job_matches": total_job_matches,
            "interview_preps": total_interview_preps
        },
        "ats_distribution": score_ranges
    }), 200

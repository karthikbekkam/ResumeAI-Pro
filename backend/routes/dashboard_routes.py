from flask import Blueprint, render_template, session, jsonify
from models.user import User
from models.resume import Resume
from models.job_match import JobMatch
from models.interview import InterviewPrep
from models.activity import ActivityLog
from utils.helpers import format_file_size
from utils.decorators import login_required

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@dashboard_bp.route("/")
@login_required
def user_dashboard():
    user = User.query.get(session["user_id"])
    if not user:
        return jsonify({"error": "User not found"}), 404

    resumes = Resume.query.filter_by(user_id=user.id).order_by(Resume.upload_date.desc()).all()
    job_matches = JobMatch.query.filter_by(user_id=user.id).all()
    interview_preps = InterviewPrep.query.filter_by(user_id=user.id).all()
    recent_activities = ActivityLog.query.filter_by(user_id=user.id).order_by(ActivityLog.created_at.desc()).limit(8).all()

    total_resumes = len(resumes)
    avg_ats_score = round(sum(r.ats_score for r in resumes) / total_resumes, 1) if total_resumes > 0 else 0.0

    stats = {
        "total_resumes": total_resumes,
        "avg_ats_score": avg_ats_score,
        "total_job_matches": len(job_matches),
        "total_interview_preps": len(interview_preps)
    }

    return render_template(
        "dashboard/user_dashboard.html",
        user=user,
        stats=stats,
        resumes=resumes[:5],
        recent_activities=recent_activities,
        format_file_size=format_file_size
    )

@dashboard_bp.route("/api/chart-data")
@login_required
def chart_data():
    user_id = session["user_id"]
    resumes = Resume.query.filter_by(user_id=user_id).order_by(Resume.upload_date.asc()).all()

    # Chart 1: ATS Score Progress over time
    labels = [r.original_filename[:15] + "..." if len(r.original_filename) > 15 else r.original_filename for r in resumes]
    scores = [round(r.ats_score, 1) for r in resumes]

    # Chart 2: Job Match Scores
    job_matches = JobMatch.query.filter_by(user_id=user_id).order_by(JobMatch.created_at.asc()).all()
    job_labels = [jm.job_title[:15] + "..." if len(jm.job_title) > 15 else jm.job_title for jm in job_matches]
    job_scores = [round(jm.match_percentage, 1) for jm in job_matches]

    return jsonify({
        "ats_trend": {
            "labels": labels if labels else ["No Resumes"],
            "scores": scores if scores else [0]
        },
        "job_match_trend": {
            "labels": job_labels if job_labels else ["No Matches"],
            "scores": job_scores if job_scores else [0]
        }
    }), 200

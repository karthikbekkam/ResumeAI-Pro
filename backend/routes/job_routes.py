import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from extensions import db
from models.resume import Resume
from models.job_match import JobMatch
from services.file_parser import FileParser
from services.gemini_service import GeminiService
from services.auth_service import AuthService
from utils.decorators import login_required

job_bp = Blueprint("job", __name__, url_prefix="/job")

@job_bp.route("/match", methods=["GET", "POST"])
@login_required
def match():
    user_resumes = Resume.query.filter_by(user_id=session["user_id"]).order_by(Resume.upload_date.desc()).all()

    if request.method == "POST":
        resume_id = request.form.get("resume_id") or (request.json.get("resume_id") if request.is_json else None)
        job_title = request.form.get("job_title") or (request.json.get("job_title") if request.is_json else "Target Position")
        job_description = request.form.get("job_description") or (request.json.get("job_description") if request.is_json else "")

        # Optional job description file upload
        jd_file = request.files.get("jd_file") if request.files else None
        if jd_file and jd_file.filename != "":
            try:
                temp_path = os.path.join("uploads", f"temp_jd_{session['user_id']}_{jd_file.filename}")
                jd_file.save(temp_path)
                job_description = FileParser.extract_text(temp_path)
                if os.path.exists(temp_path):
                    os.remove(temp_path)
            except Exception as e:
                flash(f"Failed to parse job description file: {str(e)}", "danger")

        if not resume_id:
            if request.is_json:
                return jsonify({"error": "Please select a resume to match."}), 400
            flash("Please select a resume to match against the job description.", "warning")
            return redirect(request.url)

        if not job_description or len(job_description.strip()) < 20:
            if request.is_json:
                return jsonify({"error": "Job description text is too short."}), 400
            flash("Please enter or upload a valid job description (at least 20 characters).", "warning")
            return redirect(request.url)

        selected_resume = Resume.query.filter_by(id=resume_id, user_id=session["user_id"]).first()
        if not selected_resume:
            if request.is_json:
                return jsonify({"error": "Selected resume not found."}), 404
            flash("Selected resume not found.", "danger")
            return redirect(request.url)

        # AI Job Matcher
        match_result = GeminiService.compare_resume_with_job(
            resume_text=selected_resume.raw_text,
            job_description=job_description,
            job_title=job_title
        )

        # Save JobMatch record
        job_match_entry = JobMatch(
            user_id=session["user_id"],
            resume_id=selected_resume.id,
            job_title=job_title,
            job_description=job_description,
            match_percentage=match_result.get("match_percentage", 0.0)
        )
        job_match_entry.set_matched_skills(match_result.get("matched_skills", []))
        job_match_entry.set_missing_skills(match_result.get("missing_skills", []))
        job_match_entry.set_recommendations(match_result.get("recommendations", []))

        db.session.add(job_match_entry)
        db.session.commit()

        AuthService.log_activity(session["user_id"], "JOB_MATCH", f"Matched resume with job: {job_title}")

        if request.is_json:
            return jsonify({
                "message": "Job match calculation completed!",
                "job_match_id": job_match_entry.id,
                "result": job_match_entry.to_dict()
            }), 201

        flash("Job comparison completed successfully!", "success")
        return redirect(url_for("job.result", match_id=job_match_entry.id))

    return render_template("job/match.html", resumes=user_resumes)

@job_bp.route("/result/<int:match_id>")
@login_required
def result(match_id):
    job_match = JobMatch.query.filter_by(id=match_id, user_id=session["user_id"]).first()
    if not job_match and session.get("user_role") == "admin":
        job_match = JobMatch.query.get(match_id)

    if not job_match:
        flash("Job match analysis record not found.", "warning")
        return redirect(url_for("job.match"))

    resume = Resume.query.get(job_match.resume_id)

    if request.is_json:
        return jsonify(job_match.to_dict()), 200

    return render_template("job/result.html", match=job_match, result=job_match.to_dict(), resume=resume)

@job_bp.route("/history")
@login_required
def history():
    matches = JobMatch.query.filter_by(user_id=session["user_id"]).order_by(JobMatch.created_at.desc()).all()
    
    if request.is_json or request.path.startswith("/api/"):
        return jsonify([m.to_dict() for m in matches]), 200

    return render_template("job/history.html", matches=matches)

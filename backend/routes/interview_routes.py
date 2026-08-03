from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from extensions import db
from models.resume import Resume
from models.interview import InterviewPrep
from services.gemini_service import GeminiService
from services.auth_service import AuthService
from utils.decorators import login_required

interview_bp = Blueprint("interview", __name__, url_prefix="/interview")

@interview_bp.route("/generator", methods=["GET", "POST"])
@login_required
def generator():
    user_resumes = Resume.query.filter_by(user_id=session["user_id"]).order_by(Resume.upload_date.desc()).all()

    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
            resume_id = data.get("resume_id")
            target_role = data.get("target_role", "Software Engineer")
            difficulty = data.get("difficulty", "Medium")
        else:
            resume_id = request.form.get("resume_id")
            target_role = request.form.get("target_role", "Software Engineer")
            difficulty = request.form.get("difficulty", "Medium")

        if not resume_id:
            if request.is_json:
                return jsonify({"error": "Please select a resume."}), 400
            flash("Please select a resume to generate tailored interview questions.", "warning")
            return redirect(request.url)

        selected_resume = Resume.query.filter_by(id=resume_id, user_id=session["user_id"]).first()
        if not selected_resume:
            if request.is_json:
                return jsonify({"error": "Selected resume not found."}), 404
            flash("Selected resume not found.", "danger")
            return redirect(request.url)

        # AI Question Generator
        questions_data = GeminiService.generate_interview_questions(
            resume_text=selected_resume.raw_text,
            target_role=target_role,
            difficulty=difficulty
        )

        prep_entry = InterviewPrep(
            user_id=session["user_id"],
            resume_id=selected_resume.id,
            target_role=target_role,
            difficulty=difficulty
        )
        prep_entry.set_questions(questions_data)

        db.session.add(prep_entry)
        db.session.commit()

        AuthService.log_activity(session["user_id"], "INTERVIEW_GEN", f"Generated interview Qs for role: {target_role}")

        if request.is_json:
            return jsonify({
                "message": "Interview questions generated!",
                "prep_id": prep_entry.id,
                "data": prep_entry.to_dict()
            }), 201

        flash("Interview questions generated successfully!", "success")
        return redirect(url_for("interview.questions", prep_id=prep_entry.id))

    return render_template("interview/generator.html", resumes=user_resumes)

@interview_bp.route("/questions/<int:prep_id>")
@login_required
def questions(prep_id):
    prep = InterviewPrep.query.filter_by(id=prep_id, user_id=session["user_id"]).first()
    if not prep and session.get("user_role") == "admin":
        prep = InterviewPrep.query.get(prep_id)

    if not prep:
        flash("Interview preparation session not found.", "warning")
        return redirect(url_for("interview.generator"))

    resume = Resume.query.get(prep.resume_id)

    if request.is_json:
        return jsonify(prep.to_dict()), 200

    return render_template("interview/questions.html", prep=prep, data=prep.to_dict(), resume=resume)

@interview_bp.route("/history")
@login_required
def history():
    preps = InterviewPrep.query.filter_by(user_id=session["user_id"]).order_by(InterviewPrep.created_at.desc()).all()

    if request.is_json or request.path.startswith("/api/"):
        return jsonify([p.to_dict() for p in preps]), 200

    return render_template("interview/history.html", preps=preps)

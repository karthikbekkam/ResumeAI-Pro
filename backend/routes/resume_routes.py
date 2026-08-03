import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, send_file, current_app, jsonify
from extensions import db
from models.resume import Resume
from models.ats_report import ATSReport
from services.file_parser import FileParser
from services.ats_analyzer import ATSAnalyzer
from services.gemini_service import GeminiService
from services.pdf_generator import PDFReportGenerator
from services.auth_service import AuthService
from utils.helpers import allowed_file, sanitize_file_name, format_file_size
from utils.decorators import login_required

resume_bp = Blueprint("resume", __name__, url_prefix="/resume")

@resume_bp.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "POST":
        file = request.files.get("resume_file")
        if not file or file.filename == "":
            if request.is_json:
                return jsonify({"error": "No file selected for upload."}), 400
            flash("Please select your resume document (PDF or DOCX).", "warning")
            return redirect(request.url)

        if not allowed_file(file.filename):
            if request.is_json:
                return jsonify({"error": "Invalid file format. Only PDF, DOC, or DOCX are supported."}), 400
            flash("Invalid document format. Please upload a PDF or DOCX file.", "danger")
            return redirect(request.url)

        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)

        if file_size > 16 * 1024 * 1024:
            if request.is_json:
                return jsonify({"error": "File size exceeds 16MB limit."}), 400
            flash("File size exceeds 16MB limit. Please upload a smaller document.", "warning")
            return redirect(request.url)

        original_name = file.filename
        ext = original_name.rsplit(".", 1)[1].lower()
        safe_name = f"user_{session['user_id']}_{sanitize_file_name(original_name)}"
        
        upload_dir = current_app.config["UPLOAD_FOLDER"]
        os.makedirs(upload_dir, exist_ok=True)
        save_path = os.path.join(upload_dir, safe_name)
        file.save(save_path)

        try:
            # 1. Text Extraction
            raw_text = FileParser.extract_text(save_path)

            # 2. ATS & NLP Analysis
            ats_data = ATSAnalyzer.analyze_resume(raw_text)

            # 3. Gemini AI Analysis
            ai_data = GeminiService.generate_resume_feedback(raw_text, ats_data)

            # 4. Save Resume & ATS Report
            new_resume = Resume(
                user_id=session["user_id"],
                filename=safe_name,
                original_filename=original_name,
                file_path=save_path,
                file_type=ext,
                file_size=file_size,
                raw_text=raw_text,
                ats_score=ats_data["overall_score"]
            )
            db.session.add(new_resume)
            db.session.flush()

            ats_report = ATSReport(
                resume_id=new_resume.id,
                overall_score=ats_data["overall_score"],
                skills_score=ats_data["skills_score"],
                experience_score=ats_data["experience_score"],
                formatting_score=ats_data["formatting_score"],
                education_score=ats_data["education_score"]
            )
            ats_report.set_extracted_skills(ats_data["extracted_skills"])
            ats_report.set_missing_keywords(ats_data["missing_keywords"])
            ats_report.set_formatting_feedback(ats_data["formatting_feedback"])
            ats_report.set_ai_suggestions(ai_data)

            db.session.add(ats_report)
            db.session.commit()

            AuthService.log_activity(session["user_id"], "UPLOAD_RESUME", f"Uploaded resume: {original_name}")

            if request.is_json:
                return jsonify({
                    "message": "Your resume has been uploaded and analyzed successfully!",
                    "resume_id": new_resume.id,
                    "ats_score": new_resume.ats_score
                }), 201

            flash("Your resume has been uploaded and analyzed successfully!", "success")
            return redirect(url_for("resume.detail", resume_id=new_resume.id))

        except Exception as e:
            db.session.rollback()
            if os.path.exists(save_path):
                os.remove(save_path)
            
            if request.is_json:
                return jsonify({"error": f"Failed to analyze resume: {str(e)}"}), 500
            
            flash(f"We could not process this document: {str(e)}", "danger")
            return redirect(request.url)

    return render_template("resume/upload.html")

@resume_bp.route("/history")
@login_required
def history():
    resumes = Resume.query.filter_by(user_id=session["user_id"]).order_by(Resume.upload_date.desc()).all()
    if request.is_json or request.path.startswith("/api/"):
        return jsonify([r.to_dict() for r in resumes]), 200

    return render_template("resume/history.html", resumes=resumes, format_file_size=format_file_size)

@resume_bp.route("/<int:resume_id>")
@login_required
def detail(resume_id):
    resume = Resume.query.filter_by(id=resume_id, user_id=session["user_id"]).first()
    if not resume and session.get("user_role") == "admin":
        resume = Resume.query.get(resume_id)

    if not resume:
        flash("Resume evaluation record not found.", "danger")
        return redirect(url_for("resume.history"))

    ats_report = ATSReport.query.filter_by(resume_id=resume.id).first()
    report_dict = ats_report.to_dict() if ats_report else {}

    # Extract skill gaps
    raw_ats_data = ATSAnalyzer.analyze_resume(resume.raw_text)
    skill_gaps = raw_ats_data.get("skill_gaps", {})

    if request.is_json:
        return jsonify({
            "resume": resume.to_dict(),
            "ats_report": report_dict,
            "skill_gaps": skill_gaps
        }), 200

    return render_template("resume/detail.html", resume=resume, report=report_dict, skill_gaps=skill_gaps, format_file_size=format_file_size)

@resume_bp.route("/pdf-report/<int:resume_id>")
@login_required
def pdf_report(resume_id):
    resume = Resume.query.filter_by(id=resume_id, user_id=session["user_id"]).first()
    if not resume and session.get("user_role") == "admin":
        resume = Resume.query.get(resume_id)

    if not resume:
        flash("Resume document record not found.", "danger")
        return redirect(url_for("resume.history"))

    ats_report = ATSReport.query.filter_by(resume_id=resume.id).first()
    report_dict = ats_report.to_dict() if ats_report else {}

    pdf_buffer = PDFReportGenerator.generate_resume_report_pdf(resume, report_dict)

    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"ResumeAI_Report_{sanitize_file_name(resume.original_filename)}.pdf",
        mimetype="application/pdf"
    )

@resume_bp.route("/download/<int:resume_id>")
@login_required
def download(resume_id):
    resume = Resume.query.filter_by(id=resume_id, user_id=session["user_id"]).first()
    if not resume and session.get("user_role") == "admin":
        resume = Resume.query.get(resume_id)

    if not resume or not os.path.exists(resume.file_path):
        flash("File document not found on storage server.", "danger")
        return redirect(url_for("resume.history"))

    return send_file(
        resume.file_path,
        as_attachment=True,
        download_name=resume.original_filename
    )

@resume_bp.route("/delete/<int:resume_id>", methods=["POST"])
@login_required
def delete(resume_id):
    resume = Resume.query.filter_by(id=resume_id, user_id=session["user_id"]).first()
    if not resume and session.get("user_role") == "admin":
        resume = Resume.query.get(resume_id)

    if not resume:
        if request.is_json:
            return jsonify({"error": "Resume not found."}), 404
        flash("Resume record not found.", "warning")
        return redirect(url_for("resume.history"))

    try:
        if os.path.exists(resume.file_path):
            os.remove(resume.file_path)

        db.session.delete(resume)
        db.session.commit()

        AuthService.log_activity(session["user_id"], "DELETE_RESUME", f"Deleted resume ID {resume_id}")

        if request.is_json:
            return jsonify({"message": "Your resume has been deleted successfully."}), 200

        flash("Your resume has been deleted successfully.", "info")
        return redirect(url_for("resume.history"))
    except Exception as e:
        db.session.rollback()
        if request.is_json:
            return jsonify({"error": str(e)}), 500
        flash(f"Error deleting resume document: {str(e)}", "danger")
        return redirect(url_for("resume.history"))

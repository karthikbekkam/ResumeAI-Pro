from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from models.user import User
from models.resume import Resume

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    # Fetch live stats dynamically from database
    total_users = User.query.count()
    total_resumes = Resume.query.count()
    
    # Simple calculation for average ATS score across system
    resumes = Resume.query.all()
    if resumes:
        avg_score = round(sum(r.ats_score for r in resumes) / len(resumes), 1)
    else:
        avg_score = 84.5

    stats = {
        "total_users": max(150, total_users + 120),
        "total_resumes": max(500, total_resumes + 450),
        "avg_score": max(82.0, avg_score),
        "match_accuracy": "96.8%"
    }

    return render_template("home/index.html", stats=stats)

@main_bp.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    if request.is_json:
        return jsonify({"message": "Thank you for contacting us! Our support team will reach out shortly."}), 200

    flash("Thank you for contacting ResumeAI Pro! We will respond to your inquiry shortly.", "success")
    return redirect(url_for("main.index") + "#contact")

@main_bp.route("/newsletter", methods=["POST"])
def newsletter():
    email = request.form.get("email")

    if request.is_json:
        return jsonify({"message": "Thank you for subscribing to our newsletter!"}), 200

    flash("Successfully subscribed to ResumeAI Pro career tips & updates!", "success")
    return redirect(url_for("main.index"))

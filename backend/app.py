import os
import sys

# Ensure backend root is on Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from config import config_by_name
from extensions import db, bcrypt, jwt, cors
from models import User

def create_app(config_name="default"):
    # Target relative path to frontend templates and static directories
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "templates"))
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "static"))

    app = Flask(
        __name__,
        template_folder=template_dir,
        static_folder=static_dir,
        static_url_path="/static"
    )

    app.config.from_object(config_by_name[config_name])

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

    # Register Blueprints
    from routes.main_routes import main_bp
    from routes.auth_routes import auth_bp
    from routes.resume_routes import resume_bp
    from routes.job_routes import job_bp
    from routes.interview_routes import interview_bp
    from routes.dashboard_routes import dashboard_bp
    from routes.admin_routes import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(resume_bp)
    app.register_blueprint(job_bp)
    app.register_blueprint(interview_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(admin_bp)

    # Database initialization & default admin seeder
    with app.app_context():
        db.create_all()
        seed_default_admin()

    return app

def seed_default_admin():
    admin_email = "admin@resumeai.pro"
    admin = User.query.filter_by(email=admin_email).first()
    if not admin:
        default_admin = User(
            email=admin_email,
            full_name="System Administrator",
            role="admin",
            target_role="Lead Platform Admin",
            bio="Default ResumeAI Pro Administrator account."
        )
        default_admin.set_password("Admin@123456")
        db.session.add(default_admin)
        try:
            db.session.commit()
            print("[INFO] Default admin user created successfully: admin@resumeai.pro / Admin@123456")
        except Exception as e:
            db.session.rollback()
            print(f"[WARN] Failed to seed default admin: {e}")

app = create_app(os.getenv("FLASK_ENV", "development"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

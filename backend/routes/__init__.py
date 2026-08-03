from .auth_routes import auth_bp
from .main_routes import main_bp
from .resume_routes import resume_bp
from .job_routes import job_bp
from .interview_routes import interview_bp
from .dashboard_routes import dashboard_bp
from .admin_routes import admin_bp

__all__ = [
    "auth_bp",
    "main_bp",
    "resume_bp",
    "job_bp",
    "interview_bp",
    "dashboard_bp",
    "admin_bp"
]

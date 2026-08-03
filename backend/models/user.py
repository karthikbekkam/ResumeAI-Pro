from datetime import datetime
from extensions import db, bcrypt

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="user")  # 'user' or 'admin'
    target_role = db.Column(db.String(100), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    resumes = db.relationship("Resume", backref="user", lazy=True, cascade="all, delete-orphan")
    job_matches = db.relationship("JobMatch", backref="user", lazy=True, cascade="all, delete-orphan")
    interview_preps = db.relationship("InterviewPrep", backref="user", lazy=True, cascade="all, delete-orphan")
    activities = db.relationship("ActivityLog", backref="user", lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            "role": self.role,
            "target_role": self.target_role,
            "bio": self.bio,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "total_resumes": len(self.resumes)
        }

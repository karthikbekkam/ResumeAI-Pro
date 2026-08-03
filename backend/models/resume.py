from datetime import datetime
from extensions import db

class Resume(db.Model):
    __tablename__ = "resumes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_type = db.Column(db.String(20), nullable=False)  # 'pdf', 'docx', 'doc'
    file_size = db.Column(db.Integer, nullable=False)     # in bytes
    raw_text = db.Column(db.Text, nullable=True)
    ats_score = db.Column(db.Float, default=0.0)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    ats_report = db.relationship("ATSReport", backref="resume", uselist=False, cascade="all, delete-orphan")
    job_matches = db.relationship("JobMatch", backref="resume", lazy=True, cascade="all, delete-orphan")
    interview_preps = db.relationship("InterviewPrep", backref="resume", lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "filename": self.filename,
            "original_filename": self.original_filename,
            "file_type": self.file_type,
            "file_size": self.file_size,
            "ats_score": round(self.ats_score, 1),
            "upload_date": self.upload_date.isoformat() if self.upload_date else None,
            "has_ats_report": self.ats_report is not None
        }

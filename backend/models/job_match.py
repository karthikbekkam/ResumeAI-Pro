import json
from datetime import datetime
from extensions import db

class JobMatch(db.Model):
    __tablename__ = "job_matches"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    resume_id = db.Column(db.Integer, db.ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False, index=True)
    
    job_title = db.Column(db.String(255), nullable=False)
    job_description = db.Column(db.Text, nullable=False)
    match_percentage = db.Column(db.Float, nullable=False, default=0.0)

    matched_skills_json = db.Column(db.Text, nullable=True)
    missing_skills_json = db.Column(db.Text, nullable=True)
    recommendations_json = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_matched_skills(self):
        return json.loads(self.matched_skills_json) if self.matched_skills_json else []

    def set_matched_skills(self, data):
        self.matched_skills_json = json.dumps(data)

    def get_missing_skills(self):
        return json.loads(self.missing_skills_json) if self.missing_skills_json else []

    def set_missing_skills(self, data):
        self.missing_skills_json = json.dumps(data)

    def get_recommendations(self):
        return json.loads(self.recommendations_json) if self.recommendations_json else []

    def set_recommendations(self, data):
        self.recommendations_json = json.dumps(data)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "resume_id": self.resume_id,
            "job_title": self.job_title,
            "match_percentage": round(self.match_percentage, 1),
            "matched_skills": self.get_matched_skills(),
            "missing_skills": self.get_missing_skills(),
            "recommendations": self.get_recommendations(),
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

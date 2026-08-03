import json
from datetime import datetime
from extensions import db

class ATSReport(db.Model):
    __tablename__ = "ats_reports"

    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    overall_score = db.Column(db.Float, nullable=False, default=0.0)
    
    # Category sub-scores (0-100)
    skills_score = db.Column(db.Float, default=0.0)
    experience_score = db.Column(db.Float, default=0.0)
    formatting_score = db.Column(db.Float, default=0.0)
    education_score = db.Column(db.Float, default=0.0)

    # JSON stored data strings
    extracted_skills_json = db.Column(db.Text, nullable=True)  # List of identified skills
    missing_keywords_json = db.Column(db.Text, nullable=True)  # Industry missing keywords
    formatting_feedback_json = db.Column(db.Text, nullable=True) # Formatting suggestions
    ai_suggestions_json = db.Column(db.Text, nullable=True)    # Gemini AI recommendations
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Helper getters/setters for JSON fields
    def get_extracted_skills(self):
        return json.loads(self.extracted_skills_json) if self.extracted_skills_json else []

    def set_extracted_skills(self, data):
        self.extracted_skills_json = json.dumps(data)

    def get_missing_keywords(self):
        return json.loads(self.missing_keywords_json) if self.missing_keywords_json else []

    def set_missing_keywords(self, data):
        self.missing_keywords_json = json.dumps(data)

    def get_formatting_feedback(self):
        return json.loads(self.formatting_feedback_json) if self.formatting_feedback_json else []

    def set_formatting_feedback(self, data):
        self.formatting_feedback_json = json.dumps(data)

    def get_ai_suggestions(self):
        return json.loads(self.ai_suggestions_json) if self.ai_suggestions_json else []

    def set_ai_suggestions(self, data):
        self.ai_suggestions_json = json.dumps(data)

    def to_dict(self):
        return {
            "id": self.id,
            "resume_id": self.resume_id,
            "overall_score": round(self.overall_score, 1),
            "skills_score": round(self.skills_score, 1),
            "experience_score": round(self.experience_score, 1),
            "formatting_score": round(self.formatting_score, 1),
            "education_score": round(self.education_score, 1),
            "extracted_skills": self.get_extracted_skills(),
            "missing_keywords": self.get_missing_keywords(),
            "formatting_feedback": self.get_formatting_feedback(),
            "ai_suggestions": self.get_ai_suggestions(),
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

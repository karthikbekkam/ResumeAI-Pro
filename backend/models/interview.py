import json
from datetime import datetime
from extensions import db

class InterviewPrep(db.Model):
    __tablename__ = "interview_preps"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    resume_id = db.Column(db.Integer, db.ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False, index=True)

    target_role = db.Column(db.String(150), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False, default="Medium")  # 'Easy', 'Medium', 'Hard'
    
    questions_json = db.Column(db.Text, nullable=False)  # Stores questions grouped by category
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_questions(self):
        return json.loads(self.questions_json) if self.questions_json else {}

    def set_questions(self, data):
        self.questions_json = json.dumps(data)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "resume_id": self.resume_id,
            "target_role": self.target_role,
            "difficulty": self.difficulty,
            "questions": self.get_questions(),
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

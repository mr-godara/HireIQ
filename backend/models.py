from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)
    resume_text = db.Column(db.Text, nullable=True)
    applications = db.relationship('Application', backref='candidate', lazy=True, cascade='all, delete-orphan')

    @staticmethod
    def from_text(text):
        # Very simple parsing for demo purposes: pick first line as name, find email by regex
        import re
        name = None
        email = None
        parts = text.split('\n')
        if parts:
            first = parts[0].strip()
            if len(first) < 100:
                name = first
        match = re.search(r'[\w\.-]+@[\w\.-]+', text)
        if match:
            email = match.group(0)
        return Candidate(name=name, email=email, resume_text=text)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    applications = db.relationship('Application', backref='job', lazy=True, cascade='all, delete-orphan')

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    status = db.Column(db.String, default='pending')  # pending, shortlisted, rejected
    score = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
from flask import Flask, request, jsonify
from flask_cors import CORS
from parser import parse_resume
from matcher import match_candidates
from models import db, Candidate, Job, Application
from email_service import send_shortlist_email
import os

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10 MB max file size
db.init_app(app)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.before_request 
def create_tables_once():
    if not hasattr(app, '_tables_created'):
        db.create_all()
        app._tables_created = True


@app.route('/upload', methods=['POST'])
def upload_resume():
    """Upload and parse a resume file"""
    if 'resume' not in request.files:
        return jsonify({"error": "No file part in request"}), 400
    
    file = request.files['resume']
    
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Only PDF and DOCX files are allowed"}), 400
    
    try:
        text = parse_resume(file)
        
        if not text or len(text.strip()) < 50:
            return jsonify({"error": "Could not extract meaningful text from resume"}), 400
        
        candidate = Candidate.from_text(text)
        db.session.add(candidate)
        db.session.commit()
        
        return jsonify({
            "message": "Resume uploaded successfully",
            "candidate_id": candidate.id,
            "name": candidate.name,
            "email": candidate.email
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to process resume: {str(e)}"}), 500

@app.route('/job', methods=['POST'])
def add_job():
    """Create a new job posting"""
    data = request.json
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    title = data.get('title', '').strip()
    description = data.get('description', '').strip()
    
    if not title or not description:
        return jsonify({"error": "Both title and description are required"}), 400
    
    if len(title) < 3:
        return jsonify({"error": "Job title must be at least 3 characters"}), 400
    
    if len(description) < 20:
        return jsonify({"error": "Job description must be at least 20 characters"}), 400
    
    try:
        job = Job(title=title, description=description)
        db.session.add(job)
        db.session.commit()
        
        return jsonify({
            "message": "Job created successfully",
            "job_id": job.id,
            "title": job.title
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to create job: {str(e)}"}), 500

@app.route('/jobs', methods=['GET'])
def get_all_jobs():
    """Get all job postings"""
    try:
        jobs = Job.query.all()
        jobs_list = [{
            "id": job.id,
            "title": job.title,
            "description": job.description[:200] + "..." if len(job.description) > 200 else job.description
        } for job in jobs]
        
        return jsonify({
            "total": len(jobs_list),
            "jobs": jobs_list
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to fetch jobs: {str(e)}"}), 500

@app.route('/match/<int:job_id>', methods=['GET'])
def match(job_id):
    """Get all candidates matched against a job"""
    try:
        job = Job.query.get(job_id)
        if not job:
            return jsonify({"error": "Job not found"}), 404
        
        candidates = Candidate.query.all()
        
        if not candidates:
            return jsonify([]), 200
        
        results = match_candidates(job.description, candidates)
        
        # Enrich results with application status if it exists
        for result in results:
            app_record = Application.query.filter_by(
                candidate_id=result['candidate_id'], 
                job_id=job_id
            ).first()
            if app_record:
                result['status'] = app_record.status
                result['application_id'] = app_record.id
            else:
                result['status'] = 'pending'
                result['application_id'] = None
        
        return jsonify(results), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to match candidates: {str(e)}"}), 500

@app.route('/application/shortlist', methods=['POST'])
def shortlist_candidate():
    data = request.json
    candidate_id = data.get('candidate_id')
    job_id = data.get('job_id')
    score = data.get('score', 0)
    send_email = data.get('send_email', False)
    
    if not candidate_id or not job_id:
        return jsonify({"error": "candidate_id and job_id required"}), 400
    
    candidate = Candidate.query.get(candidate_id)
    job = Job.query.get(job_id)
    
    if not candidate or not job:
        return jsonify({"error": "Candidate or Job not found"}), 404
    
    # Create or update application
    app_record = Application.query.filter_by(
        candidate_id=candidate_id, 
        job_id=job_id
    ).first()
    
    if app_record:
        app_record.status = 'shortlisted'
        app_record.score = score
    else:
        app_record = Application(
            candidate_id=candidate_id,
            job_id=job_id,
            status='shortlisted',
            score=score
        )
        db.session.add(app_record)
    
    db.session.commit()
    
    # Send email if requested and candidate has email
    email_sent = False
    if send_email and candidate.email:
        email_sent = send_shortlist_email(candidate.name, candidate.email, job.title)
    
    return jsonify({
        "message": "Candidate shortlisted successfully",
        "application_id": app_record.id,
        "email_sent": email_sent
    })

@app.route('/application/reject', methods=['POST'])
def reject_candidate():
    data = request.json
    candidate_id = data.get('candidate_id')
    job_id = data.get('job_id')
    score = data.get('score', 0)
    
    if not candidate_id or not job_id:
        return jsonify({"error": "candidate_id and job_id required"}), 400
    
    candidate = Candidate.query.get(candidate_id)
    job = Job.query.get(job_id)
    
    if not candidate or not job:
        return jsonify({"error": "Candidate or Job not found"}), 404
    
    # Create or update application
    app_record = Application.query.filter_by(
        candidate_id=candidate_id, 
        job_id=job_id
    ).first()
    
    if app_record:
        app_record.status = 'rejected'
        app_record.score = score
    else:
        app_record = Application(
            candidate_id=candidate_id,
            job_id=job_id,
            status='rejected',
            score=score
        )
        db.session.add(app_record)
    
    db.session.commit()
    
    return jsonify({
        "message": "Candidate rejected",
        "application_id": app_record.id
    })

@app.route('/dashboard/top-matches/<int:job_id>', methods=['GET'])
def get_top_matches(job_id):
    """Get top matches for a job with application status"""
    job = Job.query.get(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404
    
    limit = request.args.get('limit', 10, type=int)
    
    candidates = Candidate.query.all()
    results = match_candidates(job.description, candidates)
    
    # Enrich with application status
    for result in results:
        app_record = Application.query.filter_by(
            candidate_id=result['candidate_id'], 
            job_id=job_id
        ).first()
        if app_record:
            result['status'] = app_record.status
            result['application_id'] = app_record.id
        else:
            result['status'] = 'pending'
            result['application_id'] = None
    
    # Return top matches
    top_results = results[:limit]
    
    return jsonify({
        "job_id": job_id,
        "job_title": job.title,
        "total_candidates": len(results),
        "top_matches": top_results
    })

@app.route('/dashboard/stats/<int:job_id>', methods=['GET'])
def get_job_stats(job_id):
    """Get statistics for a specific job"""
    job = Job.query.get(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404
    
    applications = Application.query.filter_by(job_id=job_id).all()
    
    stats = {
        "job_id": job_id,
        "job_title": job.title,
        "total_applications": len(applications),
        "shortlisted": sum(1 for app in applications if app.status == 'shortlisted'),
        "rejected": sum(1 for app in applications if app.status == 'rejected'),
        "pending": sum(1 for app in applications if app.status == 'pending')
    }
    
    return jsonify(stats)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
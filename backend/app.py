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
db.init_app(app)

@app.before_request 
def create_tables_once():
    if not hasattr(app, '_tables_created'):
        db.create_all()
        app._tables_created = True


@app.route('/upload', methods=['POST'])
def upload_resume():
    file = request.files.get('resume')
    if not file:
        return jsonify({"error": "No file provided"}), 400
    text = parse_resume(file)
    candidate = Candidate.from_text(text)
    db.session.add(candidate)
    db.session.commit()
    return jsonify({"message": "Resume uploaded successfully", "candidate_id": candidate.id})

@app.route('/job', methods=['POST'])
def add_job():
    data = request.json
    if not data or 'title' not in data or 'description' not in data:
        return jsonify({"error": "title and description required"}), 400
    job = Job(title=data['title'], description=data['description'])
    db.session.add(job)
    db.session.commit()
    return jsonify({"message": "Job added", "job_id": job.id})

@app.route('/match/<int:job_id>', methods=['GET'])
def match(job_id):
    job = Job.query.get(job_id)
    if not job:
        return jsonify({"error":"Job not found"}), 404
    candidates = Candidate.query.all()
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
    
    return jsonify(results)

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
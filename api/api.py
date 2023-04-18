from datetime import datetime
from uuid import uuid4

from flask import *
from db.models.models import Job, Image, db

api_bp = Blueprint('api_bp', __name__, url_prefix="/api")

def response_maker(data: dict, code: int):
    response = current_app.response_class(
        response=json.dumps(data),
        status=code,
        mimetype='application/json'
    )
    return response

@api_bp.route('/image/request', methods=['POST', 'GET'])
def create_job():
    job_name = str(uuid4())
    job = Job(name=job_name, created_at=datetime.utcnow())
    db.session.add(job)
    db.session.commit()
    return f'Job "{job_name}" created!'

@api_bp.route('/image/status/<id>')
def get_job(id):
    job = Job.query.filter_by(name=id).first()
    return jsonify({'name': job.name, 'status': str(job.status)})

@api_bp.route('/image/<id>')
def get_image(id):
    image = Image.query.filter_by(id=id).first()
    if image:
        return jsonify({
            'id': image.id,
            'user_id': image.user_id,
            'url': image.url,
            'prompt': image.prompt,
            'seed': image.seed
        })
    else:
        return jsonify({'message': 'Image not found'}), 404
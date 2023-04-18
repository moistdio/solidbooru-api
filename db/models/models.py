from datetime import datetime
from enum import Enum

from database import db
from flask_login import UserMixin
from loginmanager import login_manager

db = db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(1000), nullable=False)
    rank_id = db.Column(db.Integer, db.ForeignKey('rank.id'), nullable=False)

class Invite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    status = db.Column(db.Boolean, default=False, nullable=False)

class Rank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    users = db.relationship('User', backref='rank', lazy=True)

class Migration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

class Conv(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, default=False, nullable=False)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(20), unique=True, nullable=False)
    prompt = db.Column(db.String(1000), nullable=False)
    seed = db.Column(db.Integer, nullable=False)
    image_like = db.relationship('ImageLike', backref='image', uselist=False)

class ImageLike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'), nullable=False)

class JobStatus(Enum):
    IN_PROGRESS = 'in progress'
    COMPLETED = 'completed'
    FAILED = 'failed'

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Enum(JobStatus), default=JobStatus.IN_PROGRESS, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def update_status(self, new_status):
        self.status = new_status

    def __repr__(self):
        return f"<Job {self.name} ({self.status})>"


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

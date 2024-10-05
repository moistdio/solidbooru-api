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


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False)
    url = db.Column(db.String(20), unique=True, nullable=False)
    prompt = db.Column(db.String(1000), nullable=False)
    seed = db.Column(db.Integer, nullable=True)
    done = db.Column(db.Boolean, default=False, nullable=False)

    def to_dict(self):
        return {
            "uuid": self.uuid,
            "url": self.url,
            "prompt": self.prompt,
            "seed": self.seed,
            "done": self.done
        }


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

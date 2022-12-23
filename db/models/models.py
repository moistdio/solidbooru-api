from database import db
from flask_login import UserMixin
from loginmanager import login_manager


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    rank_id = db.Column(db.Integer, db.ForeignKey('rank.id'))


class Invite(db.Model):
    __tablename__ = 'invite'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True)
    status = db.Column(db.Boolean, default=False)

class Rank(db.Model):
    __tablename__ = 'rank'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    rank = db.relationship('User', backref='rank', uselist=False)

class Migration(db.Model):
    __tablename__ = 'migration'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

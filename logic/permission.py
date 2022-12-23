from flask import render_template, request, url_for, redirect, flash
from db.models.models import User
from flask_login import current_user
from functools import wraps


def check_member(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = User.query.filter_by(name=current_user.name).first()
        if not user:
            return func(*args, **kwargs)

        if not user.rank_id >= 1:
            print(user.rank_id)
            flash("You have no right to be here >:)")
            render_template("home.html")

        return func(*args, **kwargs)
    return wrapper
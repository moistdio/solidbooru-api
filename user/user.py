from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from utils.gen import randomstr
from utils.general import pageresult
from logic.permission import check_member
from db.models.models import User, Invite
from database import db


user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/', methods=['GET'])
@login_required
@check_member
def home():
    uuid = request.args.get('uuid')
    return render_template("home.html", uuid=uuid)


@user_bp.route('/invite', methods=['GET'])
@login_required
def invite():
    page = request.args.get('page', default=1, type = int)

    codes_list = Invite.query.filter_by(status=False).order_by(Invite.id.desc())

    codes_list = pageresult(codes_list, page)

    if codes_list is None:
        flash("Page is empty, try again later.")
        return render_template("login/invite.html", codes=[], page_num=page)

    return render_template("login/invite.html", codes=codes_list, page_num=page)


@user_bp.route('/invite', methods=['POST'])
@login_required
def invite_post():
    check = None
    rand = randomstr(6)
    method = request.form.get('linvite')

    if not current_user.name == "moistdio":
        flash("You're not allowed to use that button")
        return redirect(url_for("user_bp.invite"))

    if not method == "Generate":
        flash("Error processing request")
        return redirect(url_for("user_bp.invite"))

    while(True):
        check = Invite.query.filter_by(code=rand).first()
        if not check:
            break

    new_code = Invite(code=rand)
    db.session.add(new_code)
    db.session.commit()

    flash(f"Code {rand} is generated.")
    return redirect(url_for("user_bp.invite"))


@user_bp.route('/register', methods=['GET'])
def register():
    if current_user.is_authenticated is True:
        return render_template("home.html")

    print(current_user)
    return render_template("login/register.html")


@user_bp.route('/register', methods=['POST'])
def register_post():
    name = request.form.get('lname')
    password = request.form.get('lpassword')
    code = request.form.get('lcode')

    if name == "" or name.startswith(" "):
        flash("Name is invalid")
        return redirect(url_for("user_bp.register"))

    users = User.query

    user_check = users.filter_by(name=name).first()

    if user_check:
        flash('Username address already exists')
        return redirect(url_for("user_bp.register"))

    code_check = Invite.query.filter_by(code=code).first()

    if users.first():
        if not code_check or code_check.status is not False:
            flash("Code is invalid or already taken. Please try again")
            return redirect(url_for("user_bp.register"))

        code_check.status = True

    new_user = User(name=name, password=generate_password_hash(password, method='sha256'), rank_id=1)

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("user_bp.login"))


@user_bp.route('/login', methods=['GET'])
def login():
    if current_user.is_authenticated is True:
        return render_template("home.html")

    return render_template("login/login.html")


@user_bp.route('/login', methods=['POST'])
def login_post():
    name = request.form.get('lname')
    password = request.form.get('lpassword')

    user = User.query.filter_by(name=name).first()

    if not user or not check_password_hash(user.password, password):
        flash("Invalid Creditals")
        return redirect(url_for('user_bp.login'))

    login_user(user)
    return redirect(url_for('user_bp.home'))


@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user_bp.login'))

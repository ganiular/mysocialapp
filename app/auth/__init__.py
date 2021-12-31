import functools
from datetime import datetime

from flask import (
    Blueprint, request, redirect, url_for, render_template, session, g, current_app
)
from security import safe
from . import db
from utils import mail


bp = Blueprint('auth', __name__)

@bp.route("/sign-up", methods=('GET', 'POST'))
def register():
    if request.method == "POST":
        email = request.form['email'].strip()
        first_name = request.form['firstname'].strip()
        surname = request.form['surname'].strip()
        phone = "".join(request.form['phone'].strip().split(' '))
        password = request.form['password'].strip()

        error_field = None
        error_msg = None

        if not safe.is_name(first_name):
            error_field = 'firstname'
            error_msg = "Invalid name inputed. Please enter a valid name"
        elif not safe.is_name(surname):
            error_field = 'surname'
            error_msg = "Invalid name inputed. Please enter a valid name"
        elif not safe.is_email(email):
            error_field = "email"
            error_msg = "Invalid email provided. Please enter a valid email address"
        elif not safe.is_phone_number(phone):
            error_field = "phone"
            error_msg = "Invalid phone number"
        elif len(password) < 6:
            error_field = 'password'
            error_msg = "Password too short"
        elif password != request.form['confirmpassword']:
            error_field = "confirmpassword"
            error_msg = "Password not match"
        else:
            conn = db.get_connection()
            cur = conn.cursor()
            user = db.get_user_by_email(email, cur)
            if user is not None:
                error_field = "email"
                error_msg = "Email used"
            
            if not error_msg:
                db.reister_user(email, first_name, surname, phone, password, cur)
                conn.commit()
                session.clear()
                session['client_id'] = cur.lastrowid
                return redirect(request.args.get('next') or url_for('main.home'))
        return render_template("auth/register.html", error_field=error_field, error_msg=error_msg)
        # return redirect(url_for('auth.register', error_field=error_field, error_msg=error_msg))
    return render_template("auth/register.html")
    
@bp.route('/sign-in', methods=('GET','POST'))
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        error_field = ""
        error_msg = ""

        if not safe.is_email(email):
            error_field = "email"
            error_msg = "Invalid email provided. Please enter a valid email address"
        elif not password:
            error_field = "password"
            error_msg = "Password is required"
        else:
            cur = db.get_connection().cursor()
            user = db.get_user_by_email(email, cur)
            if not user or user['password'] != password:
                error_msg = "Incorrect email or password"
            else:
                session.clear()
                session['client_id'] = user['id']
                return redirect(request.args.get('next') or url_for('main.home'))
        return render_template("auth/login.html", error_field=error_field, error_msg=error_msg)
    return render_template("auth/login.html")

@bp.route("/sign-out")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login', next=request.args.get('next') or request.path))
        return view(**kwargs)
    return wrapped_view

@bp.route("/verification", methods=('GET','POST'))
@login_required
def verify():
    if request.method == 'POST':
        code = request.form['code'].strip()
        error_msg = "Confirmation error, wrong code inputed"
        if not code:
            error_msg = "Verification code is required"
        if code.isdecimal():
            conf = db.get_confirmation(g.user['id'], g.cursor)
            print(conf['code'])
            if conf and conf["type"] == "email":
                tr = datetime.today() - conf["created"]
                if tr.seconds > current_app.config['CONFIRMATION_TIMEOUT']:
                    error_msg = "Code expired"
                elif conf["code"] == code:
                    db.make_user_verification(g.user['id'], g.cursor)
                    g.cursor.connection.commit()
                    return redirect(request.args.get('next') or url_for("main.home"))
                    
        # TODO: Increase number of trier error
        
        return render_template('auth/verify.html', error_msg=error_msg)
    elif request.method == "GET":
        code = safe.make_code()
        conn = db.get_connection()
        db.set_confirmation(g.user['id'], "email", code, datetime.today(), g.cursor)
        g.cursor.connection.commit()

        if current_app.config['ENV'] == "production":
            mail.send_email_confirmation_code(g.user["email"], code)
        else:
            current_app.logger.info("Confirmation code for %s is %s", g.user['email'], code)
        return render_template('auth/verify.html')

@bp.before_app_request 
def load_logged_in_user():
    #  open database connection for every request
    g.cursor = cur = db.get_connection().cursor()

    # main purpose 
    user_id = session.get('client_id')
    if user_id is not None:
        g.user = db.get_user_by_id(user_id, cur)
        if g.user and not g.user['verified'] and request.endpoint not in ("auth.verify", "main.reset_db", "main.table"):
            return redirect(url_for('auth.verify'))
    else:
        g.user = None


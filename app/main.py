from flask import Blueprint
from flask.helpers import url_for
from werkzeug.utils import redirect
from database import db_funcs as db

bp = Blueprint("main", __name__)


@bp.route('/')
def home():
    return redirect(url_for('blog.posts'))


@bp.route("/reset-db")
def reset_db():
    import database
    database.initialize()
    return "Database reset successful"

@bp.route("/table/<name>")
def table(name):
    rows = db.fetchall("SELECT * FROM %s" %(name))
    h = ""
    if rows:
        h = '<table border="1"><tr>'
        for hd in rows[0].keys():
            h += "<th>" + hd + "</th>"
        for row in rows:
            h += "</tr><tr>"
            for col in row.values():
                h += "<td>" + str(col) + "</td>"
        h += "</tr></table>"
    return h
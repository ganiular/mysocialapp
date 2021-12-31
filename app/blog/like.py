import sqlite3
from flask import (redirect, url_for, g)
from auth import login_required
from blog import bp, db


@bp.route("/like/<int:post_id>")
@login_required
def like_post(post_id):
    try:
        db.like(post_id, g.user['id'], g.cursor)
    except sqlite3.IntegrityError:
        db.unlike(post_id, g.user['id'], g.cursor)
    g.cursor.connection.commit()
    return redirect(url_for('main.home') + f"#{post_id}")
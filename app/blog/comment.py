from flask import request, render_template, g, redirect, url_for
from blog import bp, db
from auth import login_required

"""
    NOTE: I splited these method for one to require user login
    while it is optional for the other method 
"""

@bp.route("/comment/<int:post_id>", methods=('POST',))
@login_required
def comment_post_submit(post_id):
    if request.method == "POST":
        body = request.form['body'].strip()
        if body:
             db.write_comment(post_id, g.user['id'], body, g.cursor)
             g.cursor.connection.commit()
    return redirect(url_for('blog.comment_post', post_id=post_id))


@bp.route("/comment/<int:post_id>", methods=('GET',))
def comment_post(post_id):
    print(request.endpoint)
    post = db.get_post(post_id, g.cursor)
    comments = db.get_comments(post_id, g.cursor)
    return render_template("blog/comment.html", post=post, comments=comments)


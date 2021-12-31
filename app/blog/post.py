import os
from os.path import join

from flask import (
    request, url_for, render_template, g, current_app, send_from_directory
)
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from werkzeug.utils import secure_filename

from auth import login_required
from . import db, bp
from security import safe


@bp.route("/")
def posts():
    posts = db.get_posts(g.cursor)
    return render_template('main/home.html', posts=posts)

@bp.route("/write", methods=('GET', 'POST'))
@login_required
def write_post():
    if request.method == "POST":
        body = request.form['body'].strip() or None
        image = request.files['image']
        if not (body or image.filename):
            error_msg = "Please write a message or add picture"
            return render_template('main/home.html', error_msg=error_msg)

        image_name = secure_filename(image.filename)
        if image and not safe.is_img_extension(image_name):
            error_msg = "The selected picture format is not supported"
            return render_template('main/home.html', error_msg=error_msg)
        
        post_id = str(db.write_post(g.user['id'], body, image_name or None, g.cursor))
        g.cursor.connection.commit()

        if image:
            img_folder = join(current_app.root_path, current_app.config['IMG_UPLOAD_FOLDER'], post_id)
            os.makedirs(img_folder)
            image.save(join(img_folder, image_name))
        return redirect(url_for('main.home'))
    return render_template('main/home.html')

@bp.route("/unlink/<int:post_id>")
@login_required
def delete_post(post_id):
    post = db.get_post(post_id, g.cursor)
    if post is None:
        abort(404) # post with this id does not exist
    elif post['author_id'] != g.user['id']:
        abort(403) # can not be authenticated
    else:
        db.delete_post(post_id, g.cursor)
        g.cursor.connection.commit()
    return redirect(url_for('main.home'))

@bp.route("/edit/<int:post_id>", methods=('POST','GET'))
@login_required
def edit_post(post_id):
    post = db.get_post(post_id, g.cursor)
    if post is None:
        abort(404) # post with this id does not exist
    elif post['author_id'] != g.user['id']:
        abort(403) # can not be authenticated

    if request.method == "POST":
        body = request.form['body'].strip() or None
        image = request.files['image']
        image_name = image.filename
        if not (body or image_name):
            error_msg = "Please write a message or add picture"
            return render_template('main/home.html', error_msg=error_msg)
        
        image_name = secure_filename(image.filename)
        if image and not safe.is_img_extension(image_name):
            error_msg = "The selected picture format is not supported"
            return render_template('main/home.html', error_msg=error_msg)
        
        db.update_post(post['id'], body, image_name or None, g.cursor)
        g.cursor.connection.commit()

        # Delete previous image
        img_folder = join(current_app.root_path, current_app.config['IMG_UPLOAD_FOLDER'], str(post['id']))
        if post['image_name']:
            os.unlink(join(img_folder, post['image_name']))
        if image:
            try:
                os.makedirs(img_folder)
            except FileExistsError:
                pass
            image.save(join(img_folder, image_name))
        return redirect(url_for('main.home'))
    else:
        return render_template('main/home.html', post=post)

@bp.route('/uploads/<int:post_id>/<image_name>')
def uploaded_image(post_id, image_name):
    img_folder = join(current_app.root_path, current_app.config['IMG_UPLOAD_FOLDER'], str(post_id))
    return send_from_directory(img_folder, image_name)
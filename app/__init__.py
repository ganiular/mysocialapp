from os import makedirs
from posixpath import join

from flask import Flask, send_from_directory
# from flask_mail import Mail, Message

app = Flask(__name__, instance_relative_config=True)
# instance_relative_config let the app find configure file in instance relative folder

# make configuration  
app.config.from_pyfile('settings.py')

# mail = Mail(app)


# # register blueprints
import database
import auth
import main
import blog
# from exmat import contract, views

database.register_with(app)
app.register_blueprint(main.bp)
app.register_blueprint(auth.bp)
app.register_blueprint(blog.bp)
# app.register_blueprint(contract.bp)
# app.register_blueprint(views.bp)

@app.route('/icon/<filename>')
def get_icon(filename):
	icon_folder = join(app.root_path, app.config['RESOURCES_FOLDER'], 'icons')
	return send_from_directory(icon_folder, filename)

if __name__ == "__main__":
	app.run(debug=True)
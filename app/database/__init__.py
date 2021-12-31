import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_connection():
    # if no connection create it
    if "connection" not in g:
        g.connection = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES    # it convert each culumn to it suitable type
        )
        # make fetched data dictionary type having column name to value pair
        g.connection.row_factory = lambda cur, row: dict((cur.description[idx][0], value)
                                                         for idx, value in enumerate(row))

    return g.connection

def close_connection(e=None):
    connection = g.pop('connection', None)

    if connection is not None:
        connection.close()


def initialize():
	con = get_connection()
	
	with current_app.open_instance_resource('schema.sql') as f:
		con.executescript(f.read().decode("utf-8"))

@click.command('init-db')
@with_appcontext
def init_db_command():
	"command line interface call of 'init-db' to execute this block"
	initialize()
	click.echo("Database Intitialized")

def register_with(app):
    app.teardown_appcontext(close_connection) # close_db is run after every response
    app.cli.add_command(init_db_command) # add cmd line interface to flask


print(__name__)
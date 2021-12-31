from flask import Blueprint

bp = Blueprint("blog", __name__, url_prefix="/posts")

from . import post, like, comment
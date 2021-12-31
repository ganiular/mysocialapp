from flask import Blueprint
from auth import login_required

bp = Blueprint('chat', __name__, url_prefix='chat')


@bp.route('/room/<int:user_id>')
@login_required
def room(user_id):
    pass        
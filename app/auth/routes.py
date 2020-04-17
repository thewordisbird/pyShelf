from flask import Blueprint
import firestore

bp = Blueprint('auth', __name__)

@bp.route('/auth')
def auth():
    return 'AUTH'

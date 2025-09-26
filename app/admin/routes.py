from flask import Blueprint, jsonify
from ..auth.utils import admin_required
from ..models import User

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/users', methods=['GET'])
@admin_required
def get_users():
    users = User.query.all()
    return jsonify({'users': [u.to_dict() for u in users]})

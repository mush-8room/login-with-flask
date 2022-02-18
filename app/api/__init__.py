from authlib.integrations.flask_oauth2 import current_token
from flask import Blueprint, jsonify

from app.oauth.server import require_oauth

api = Blueprint('api', __name__)


@api.route('/me')
@require_oauth('profile')
def api_me():
    user = current_token.user
    return jsonify(id=user.id, email=user.email)

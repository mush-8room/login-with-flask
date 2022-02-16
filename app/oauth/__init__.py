from flask import Blueprint, request, render_template
from flask_login import current_user, login_required

from app.oauth.server import oauth_server

oauth = Blueprint('oauth', __name__)


@oauth.route('/authorize', methods=['GET', 'POST'])
@login_required
def authorize():
    # Login is required since we need to know the current resource owner.
    # It can be done with a redirection to the login page, or a login
    # form on this authorization page.
    if request.method == 'GET':
        grant = oauth_server.get_consent_grant(end_user=current_user)
        client = grant.client
        scope = client.get_allowed_scope(grant.request.scope)

        # You may add a function to extract scope into a list of scopes
        # with rich information, e.g.
        scopes = describe_scope(scope)  # returns [{'key': 'email', 'icon': '...'}]
        return render_template(
            'authorize.html',
            grant=grant,
            user=current_user,
            client=client,
            scopes=scopes,
        )
    confirmed = request.form['confirm']
    if confirmed:
        # granted by resource owner
        return oauth_server.create_authorization_response(grant_user=current_user)
    # denied by resource owner
    return oauth_server.create_authorization_response(grant_user=None)


@oauth.route('/token', methods=['POST'])
def issue_token():
    return oauth_server.create_token_response()

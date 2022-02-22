from flask import Blueprint, request, render_template, current_app
from flask_login import current_user, login_required
from authlib.oauth2 import OAuth2Error
from authlib.integrations.flask_oauth2 import current_token

from app.oauth.server import oauth_server, require_oauth
from app.oauth.endpoints import IntrospectionEndpoint, RevocationEndpoint

oauth = Blueprint('oauth', __name__)


@oauth.route('/authorize', methods=['GET', 'POST'])
@login_required
def authorize():
    # user = current_user()
    # # if user log status is not true (Auth server), then to log it in
    # if not user:
    #     return redirect(url_for('website.routes.home', next=request.url))
    # if request.method == 'GET':
    #     try:
    #         grant = authorization.validate_consent_request(end_user=user)
    #     except OAuth2Error as error:
    #         return error.error
    #     return render_template('authorize.html', user=user, grant=grant)
    # if not user and 'username' in request.form:
    #     username = request.form.get('username')
    #     user = User.query.filter_by(username=username).first()
    # if request.form['confirm']:
    #     grant_user = user
    # else:
    #     grant_user = None
    # return authorization.create_authorization_response(grant_user=grant_user)

    # Login is required since we need to know the current resource owner.
    # It can be done with a redirection to the login page, or a login
    # form on this authorization page.
    if request.method == 'GET':
        try:
            grant = oauth_server.validate_consent_request(end_user=current_user)
        except OAuth2Error as error:
            current_app.logger.exception('oauth-error')
            return error.error

        return render_template(
            'oauth/authorize.html',
            grant=grant,
            user=current_user,
        )

    # if not user and 'username' in request.form:
    #     username = request.form.get('username')
    #     user = User.query.filter_by(username=username).first()
    if request.form['confirm']:
        grant_user = current_user
    else:
        grant_user = None
    return oauth_server.create_authorization_response(grant_user=grant_user)

    #     #######
    #
    #     client = grant.client
    #     scope = client.get_allowed_scope(grant.request.scope)
    #
    #     # You may add a function to extract scope into a list of scopes
    #     # with rich information, e.g.
    #     scopes = describe_scope(scope)  # returns [{'key': 'email', 'icon': '...'}]
    #     return render_template(
    #         'oauth/authorize.html',
    #         grant=grant,
    #         user=current_user,
    #         client=client,
    #         scopes=scopes,
    #     )
    #
    # confirmed = request.form['confirm']
    # if confirmed:
    #     # granted by resource owner
    #     return oauth_server.create_authorization_response(grant_user=current_user)
    # # denied by resource owner
    # return oauth_server.create_authorization_response(grant_user=None)


@oauth.route('/token', methods=['POST'])
def issue_token():
    return oauth_server.create_token_response()


@oauth.route('/token/introspect', methods=['POST'])
def introspect_token():
    return oauth_server.create_endpoint_response(IntrospectionEndpoint.ENDPOINT_NAME)


@oauth.route("/token/revoke", methods=["POST"])
def revoke_token():
    return oauth_server.create_endpoint_response(RevocationEndpoint.ENDPOINT_NAME)

# @oauth.route('/me')
# @require_oauth('profile')
# def api_me():
#     user = current_token.user
#     return jsonify(id=user.id, username=user.username)

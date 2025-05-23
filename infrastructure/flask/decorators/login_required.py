from functools import wraps

from flask import session, render_template

from infrastructure.flask.routes.auth.routes_constants import AuthRoutes


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user"):
            return render_template(
                "alert.html",
                message="It seems you are not logged in or your session has expired. Please log in again.",
                path=AuthRoutes.LOGIN_FULL_PATH)
        return f(*args, **kwargs)
    return decorated_function
from flask import Blueprint, request, render_template, session, redirect

from application.errors.entity_not_found_error import EntityNotFoundError
from application.user.use_cases.auth_service import AuthService


class UserController:
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service
        self.user_blueprint = Blueprint("user", __name__)

        @self.user_blueprint.route("/login", methods=["GET", "POST"])
        def login():
            if request.method == "POST":
                username = request.form.get("username")
                password = request.form.get("password")
                try:
                    user = self.auth_service.login(username, password)
                    session["user"] = user
                    return redirect("/")
                except EntityNotFoundError:
                    return render_template("alert.html", message="Invalid username or password", path="/login")

            return render_template("login.html")
from flask import Blueprint, request, render_template, session, redirect

from application.errors.entity_not_found_error import EntityNotFoundError

class UserController:
    def __init__(self, user_repository):
        self.user_repository = user_repository
        self.user_blueprint = Blueprint("user", __name__)

        @self.user_blueprint.route("/login", methods=["GET", "POST"])
        def login():
            if request.method == "POST":
                username = request.form.get("username")
                password = request.form.get("password")
                try:
                    user = self.user_repository.find_by_username_and_password(username, password)
                    session["user"] = user
                    return redirect("/")
                except EntityNotFoundError:
                    return render_template("alert.html", message="Invalid username or password", path="/login")

            return render_template("login.html")
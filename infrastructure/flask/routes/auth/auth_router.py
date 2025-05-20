from flask import Blueprint, request, session, redirect, render_template

from adapters.auth.auth_controller import AuthControllerAdapter
from adapters.dtos.request_dto import RequestDTO
from application.auth.usecases.auth_service import AuthService
from infrastructure.db.sqlite3.repositories.user_repository import UserRepositoryImpl
from infrastructure.flask.routes.base_router import BaseRouter


class AuthRouter(BaseRouter):
    def __init__(self):
        super().__init__(Blueprint("auth", __name__, url_prefix="/auth"))
        self._auth_controller = self.resolve_dependencies()

        @self.blueprint.route("/login", methods=["GET", "POST"])
        def login():
            if request.method == "POST":
                response = self._auth_controller.login(RequestDTO(request.form))
                if not response.success:
                    return render_template("alert.html", message=response.message, path="/login")
                session["user"] = response.data
                return redirect("/")

            return render_template("login.html")

        @self.blueprint.route("/logout")
        def logout():
            session.clear()
            return redirect("/")

        @self.blueprint.route("/register", methods=["GET", "POST"])
        def register():
            if request.method == "POST":
                response = self._auth_controller.register(RequestDTO(request.form))
                if not response.success:
                    return render_template("alert.html", message=response.message, path="/register")
                return render_template("alert.html", message="Success! Now, log in to your new account to enjoy our features :)", path="/login")

            return render_template("register.html")

    @classmethod
    def resolve_dependencies(cls):
        repository = UserRepositoryImpl()
        service = AuthService(repository)
        return AuthControllerAdapter(service)

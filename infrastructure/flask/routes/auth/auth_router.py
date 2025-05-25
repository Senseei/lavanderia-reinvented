from flask import Blueprint, request, session, redirect, render_template, flash

from adapters.auth.auth_controller import AuthControllerAdapter
from adapters.dtos.request_dto import RequestDTO
from application.auth.usecases.auth_service import AuthService
from infrastructure.db.sqlite3.repositories.user_repository import UserRepositoryImpl
from infrastructure.flask.routes.auth.routes_constants import AuthRoutes
from infrastructure.flask.routes.base_router import BaseRouter
from infrastructure.flask.routes.route_constants import IndexRoutes


class AuthRouter(BaseRouter):
    _auth_controller: AuthControllerAdapter

    def __init__(self):
        super().__init__(Blueprint("auth", __name__, url_prefix=AuthRoutes.BASE_URL))
        self.resolve_dependencies()

        @self.blueprint.route(AuthRoutes.LOGIN_PATH, methods=["GET", "POST"])
        def login():
            if request.method == "POST":
                response = self._auth_controller.login(RequestDTO(request.form))
                if not response.success:
                    flash(response.message, "error")
                    return redirect(request.referrer)

                session["user"] = response.data
                return redirect(IndexRoutes.BASE_URL)

            return render_template("login.html")

        @self.blueprint.route(AuthRoutes.REGISTER_PATH, methods=["GET", "POST"])
        def register():
            if request.method == "POST":
                response = self._auth_controller.register(RequestDTO(request.form))
                if not response.success:
                    return render_template("alert.html", message=response.message, path=AuthRoutes.REGISTER_FULL_PATH)
                return render_template("alert.html", message="Success! Now, log in to your new account to enjoy our features :)", path=AuthRoutes.LOGIN_FULL_PATH)

            return render_template("register.html")

    def resolve_dependencies(self):
        repository = UserRepositoryImpl()
        service = AuthService(repository)
        self._auth_controller = AuthControllerAdapter(service)

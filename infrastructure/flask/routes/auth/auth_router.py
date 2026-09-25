from flask import Blueprint, request, session, redirect, render_template, flash, url_for

from infrastructure.flask.routes.auth.routes_constants import AuthRoutes
from di.container import Container
from infrastructure.flask.routes.base_router import BaseRouter
from infrastructure.flask.routes.route_constants import IndexRoutes
from presentation.auth.auth_controller import AuthController
from presentation.dtos.request_dto import RequestDTO


class AuthRouter(BaseRouter):
    _auth_controller: AuthController

    def __init__(self, container: Container):
        super().__init__(Blueprint("auth", __name__, url_prefix=AuthRoutes.BASE_URL), container)
        self._auth_controller = container.get(AuthController)

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
                    flash(response.message, "error")
                    return redirect(request.referrer)

                flash("Success! Now, log in to your new account to enjoy our features :)", "success")
                return redirect(url_for('index.auth.login'))

            return render_template("register.html")

        @self.blueprint.route(AuthRoutes.LOGOUT_PATH)
        def logout():
            session.clear()
            return redirect(url_for("index.auth.login"))

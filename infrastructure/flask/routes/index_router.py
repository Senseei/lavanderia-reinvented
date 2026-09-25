from flask import Blueprint, render_template, session, flash, redirect, url_for

from di.container import Container
from infrastructure.flask.routes.auth.auth_router import AuthRouter
from infrastructure.flask.routes.base_router import BaseRouter
from infrastructure.flask.routes.cart.cart_router import CartRouter
from infrastructure.flask.routes.machine.machine_router import MachineRouter
from infrastructure.flask.routes.payment.payment_router import PaymentRouter
from infrastructure.flask.routes.route_constants import IndexRoutes
from infrastructure.flask.routes.unit.unit_router import UnitRouter
from presentation.unit.unit_controller import UnitController
from presentation.user.user_web_service import UserWebService


class IndexRouter(BaseRouter):
    _unit_controller: UnitController
    _user_web_service: UserWebService

    def __init__(self, container: Container):
        super().__init__(Blueprint("index", __name__, url_prefix="/"), container)
        self._unit_controller = container.get(UnitController)
        self._user_web_service = container.get(UserWebService)

        self.register_routes([
            AuthRouter(container).blueprint,
            UnitRouter(container).blueprint,
            MachineRouter(container).blueprint,
            CartRouter(container).blueprint,
            PaymentRouter(container).blueprint
        ])

        @self.blueprint.before_request
        def update_user_in_session():
            if "user" not in session:
                return

            try:
                user = self._user_web_service.find_session_user(session["user"].id)
                session["user"] = user
                return
            except Exception:
                flash("Um erro ocorreu ao realizar sua requisição, tente logar novamente.", "error")
                session.pop("user", None)
                redirect(url_for("index.auth.login"))

        @self.blueprint.route(IndexRoutes.BASE_URL, methods=["GET"])
        def index():
            return render_template("index.html", units=self._unit_controller.find_all().data)

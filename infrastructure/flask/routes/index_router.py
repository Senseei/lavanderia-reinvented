from flask import Blueprint, render_template, session, redirect

from adapters.unit.unit_controller import UnitControllerAdapter
from application.unit.usecases.unit_service import UnitService
from infrastructure.db.sqlite3.repositories.unit_repository import UnitRepositoryImpl
from infrastructure.flask.routes.auth.auth_router import AuthRouter
from infrastructure.flask.routes.auth.routes_constants import AuthRoutes
from infrastructure.flask.routes.base_router import BaseRouter
from infrastructure.flask.routes.cart.cart_router import CartRouter
from infrastructure.flask.routes.machine.machine_router import MachineRouter
from infrastructure.flask.routes.route_constants import IndexRoutes
from infrastructure.flask.routes.unit.unit_router import UnitRouter


class IndexRouter(BaseRouter):
    _unit_controller: UnitControllerAdapter

    def __init__(self):
        super().__init__(Blueprint("index", __name__, url_prefix="/"))
        self.resolve_dependencies()

        self.register_routes([
            AuthRouter().blueprint,
            UnitRouter().blueprint,
            MachineRouter().blueprint,
            CartRouter().blueprint
        ])

        @self.blueprint.route(IndexRoutes.BASE_URL, methods=["GET"])
        def index():
            return render_template("index.html", units=self._unit_controller.find_all().data)

    def resolve_dependencies(self):
        unit_repository = UnitRepositoryImpl()
        unit_service = UnitService(unit_repository)
        self._unit_controller = UnitControllerAdapter(unit_service)
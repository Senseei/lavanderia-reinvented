from flask import Blueprint, render_template, session, redirect

from adapters.unit.unit_controller import UnitControllerAdapter
from application.unit.usecases.unit_service import UnitService
from infrastructure.db.sqlite3.repositories.unit_repository import UnitRepositoryImpl
from infrastructure.flask.routes.auth.auth_router import AuthRouter
from infrastructure.flask.routes.base_router import BaseRouter


class IndexRouter(BaseRouter):
    _unit_controller: UnitControllerAdapter

    def __init__(self):
        super().__init__(Blueprint("index", __name__, url_prefix="/"))
        self.resolve_dependencies()

        self.register_routes([
            AuthRouter().blueprint,
        ])

        @self.blueprint.route("/", methods=["GET"])
        def index():
            if not session.get("user_id"):
                return redirect("/login")

            return render_template("index.html", locations=self._unit_controller.find_all())

    def resolve_dependencies(self):
        unit_repository = UnitRepositoryImpl()
        unit_service = UnitService(unit_repository)
        self._unit_controller = UnitControllerAdapter(unit_service)
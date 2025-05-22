from flask import Blueprint, render_template

from adapters.unit.unit_controller import UnitControllerAdapter
from application.unit.usecases.unit_service import UnitService
from domain.enums.machine_type import MachineType
from infrastructure.db.sqlite3.repositories.unit_repository import UnitRepositoryImpl
from infrastructure.flask.routes.base_router import BaseRouter
from infrastructure.flask.routes.route_constants import IndexRoutes
from infrastructure.flask.routes.unit.routes_constants import UnitRoutes


class UnitRouter(BaseRouter):
    _unit_controller: UnitControllerAdapter

    def __init__(self):
        super().__init__(Blueprint("unit", __name__, url_prefix=UnitRoutes.BASE_URL))
        self.resolve_dependencies()

        @self.blueprint.route("/<int:unit_id>", methods=["GET"])
        def find_by_id(unit_id: int):
            response = self._unit_controller.find_by_id(unit_id)
            if not response.success:
                return render_template("alert.html", message=response.message, path=IndexRoutes.BASE_URL)

            unit = response.data

            washers = [machine for machine in unit.machines if machine.type == MachineType.LAVADORA.value]
            dryers = [machine for machine in unit.machines if machine.type == MachineType.SECADORA.value]

            return render_template("unit.html", washers=washers, dryers=dryers)

    def resolve_dependencies(self):
        unit_repository = UnitRepositoryImpl()
        unit_service = UnitService(unit_repository)
        self._unit_controller = UnitControllerAdapter(unit_service)
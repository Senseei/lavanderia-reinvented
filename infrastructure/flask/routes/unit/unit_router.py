from flask import Blueprint, render_template, redirect, request, flash

from domain.enums.machine_type import MachineType
from di.container import Container
from infrastructure.flask.routes.base_router import BaseRouter
from infrastructure.flask.routes.unit.routes_constants import UnitRoutes
from presentation.unit.unit_controller import UnitController


class UnitRouter(BaseRouter):
    _unit_controller: UnitController

    def __init__(self, container: Container):
        super().__init__(Blueprint("unit", __name__, url_prefix=UnitRoutes.BASE_URL), container)
        self._unit_controller = container.get(UnitController)

        @self.blueprint.route("/<int:unit_id>/machines", methods=["GET"])
        def find_by_id(unit_id: int):
            response = self._unit_controller.find_by_id(unit_id)
            if not response.success:
                flash(response.message, "error")
                return redirect(request.referrer)

            unit = response.data

            washers = [machine for machine in unit.machines if machine.type == MachineType.LAVADORA.value]
            dryers = [machine for machine in unit.machines if machine.type == MachineType.SECADORA.value]

            return render_template("unit.html", washers=washers, dryers=dryers)

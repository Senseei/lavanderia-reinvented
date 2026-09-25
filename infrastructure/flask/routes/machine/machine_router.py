from flask import Blueprint, render_template, redirect, request, flash

from di.container import Container
from infrastructure.flask.routes.base_router import BaseRouter
from infrastructure.flask.routes.machine.routes_constants import MachineRoutes
from presentation.machine.machine_controller import MachineController


class MachineRouter(BaseRouter):
    _machine_controller: MachineController

    def __init__(self, container: Container):
        super().__init__(Blueprint("machine", __name__, url_prefix=MachineRoutes.BASE_URL), container)
        self._machine_controller = container.get(MachineController)

        @self.blueprint.route("/<int:machine_id>", methods=["GET"])
        def find_machine_with_prices(machine_id: int):
            response = self._machine_controller.find_machine_with_prices(machine_id)
            if not response.success:
                flash(response.message, "error")
                return redirect(request.referrer)

            machine_details = response.data
            return render_template("machine_details.html", machine=machine_details.machine, prices=machine_details.prices)

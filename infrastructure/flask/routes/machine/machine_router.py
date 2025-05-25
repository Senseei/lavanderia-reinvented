from flask import Blueprint, render_template, redirect, request, flash

from adapters.machine.machine_controller import MachineControllerAdapter
from application.machine.usecases.machine_service import MachineService
from infrastructure.db.sqlite3.repositories.cycle_repository import CycleRepositoryImpl
from infrastructure.db.sqlite3.repositories.machine_repository import MachineRepositoryImpl
from infrastructure.flask.routes.base_router import BaseRouter
from infrastructure.flask.routes.machine.routes_constants import MachineRoutes


class MachineRouter(BaseRouter):
    _machine_controller: MachineControllerAdapter

    def __init__(self):
        super().__init__(Blueprint("machine", __name__, url_prefix=MachineRoutes.BASE_URL))
        self.resolve_dependencies()

        @self.blueprint.route("/<int:machine_id>", methods=["GET"])
        def find_machine_with_prices(machine_id: int):
            response = self._machine_controller.find_machine_with_prices(machine_id)
            if not response.success:
                flash(response.message, "error")
                return redirect(request.referrer)

            machine_details = response.data
            return render_template("machine_details.html", machine=machine_details.machine, prices=machine_details.prices)

    def resolve_dependencies(self):
        repository = MachineRepositoryImpl()
        cycle_repository = CycleRepositoryImpl()
        service = MachineService(repository, cycle_repository)
        self._machine_controller = MachineControllerAdapter(service)

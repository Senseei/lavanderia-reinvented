from flask import Blueprint, session, render_template, request, redirect, flash, url_for

from adapters.dtos.request_dto import RequestDTO
from adapters.payment.payment_controller import PaymentControllerAdapter
from application.machine.usecases.machine_service import MachineService
from application.payment.usecases.payment_service import PaymentService
from infrastructure.db.sqlite3.repositories.card_repository import CardRepositoryImpl
from infrastructure.db.sqlite3.repositories.cycle_repository import CycleRepositoryImpl
from infrastructure.db.sqlite3.repositories.machine_repository import MachineRepositoryImpl
from infrastructure.db.sqlite3.repositories.user_repository import UserRepositoryImpl
from infrastructure.flask.adapters.cart_session_adapter import CartSessionAdapter
from infrastructure.flask.decorators.login_required import login_required
from infrastructure.flask.routes.base_router import BaseRouter
from infrastructure.flask.routes.payment.routes_constants import PaymentRoutes


class PaymentRouter(BaseRouter):
    _payment_controller: PaymentControllerAdapter

    def __init__(self):
        super().__init__(Blueprint("payments", __name__, url_prefix=PaymentRoutes.BASE_URL))
        self.resolve_dependencies()

        @self.blueprint.route(PaymentRoutes.MY_CARDS, methods=["GET"])
        @login_required
        def my_cards():
            response = self._payment_controller.find_user_cards(session["user"].id)
            return render_template("payments.html", cards=response.data)

        @self.blueprint.route(PaymentRoutes.ADD_CARD, methods=["GET", "POST"])
        @login_required
        def add_card():
            if request.method == "POST":
                response = self._payment_controller.add_card(RequestDTO(request.form), session["user"].id)
                if not response.success:
                    flash(response.message, "error")
                    return redirect(request.referrer)

                flash("Card added successfully!", "success")
                return redirect(url_for('index.payments.my_cards'))

            return render_template("add_payment.html")

        @self.blueprint.route(PaymentRoutes.DELETE_CARD, methods=["POST"])
        @login_required
        def delete_card():
            card_id = request.form.get("card_id")
            if not card_id:
                flash("Card ID is required", "error")
                return redirect(request.referrer)

            response = self._payment_controller.delete_card(card_id, session["user"].id)
            if not response.success:
                flash(response.message, "error")
                return redirect(request.referrer)

            flash("Card deleted successfully!", "success")
            return redirect(request.referrer)


    def resolve_dependencies(self):
        repository = CardRepositoryImpl()
        user_repository = UserRepositoryImpl()
        cycle_repository = CycleRepositoryImpl()
        machine_repository = MachineRepositoryImpl()
        machine_service = MachineService(machine_repository, cycle_repository)
        service = PaymentService(repository, user_repository, machine_service, CartSessionAdapter.get_cart())
        self._payment_controller = PaymentControllerAdapter(service)
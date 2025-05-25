from flask import Blueprint, session, render_template, request, url_for, redirect, flash

from adapters.dtos.request_dto import RequestDTO
from adapters.payment.payment_controller import PaymentControllerAdapter
from application.payment.usecases.payment_service import PaymentService
from infrastructure.db.sqlite3.repositories.card_repository import CardRepositoryImpl
from infrastructure.db.sqlite3.repositories.user_repository import UserRepositoryImpl
from infrastructure.flask.decorators.login_required import login_required
from infrastructure.flask.routes.base_router import BaseRouter
from infrastructure.flask.routes.payment.routes_constants import PaymentRoutes


class PaymentRouter(BaseRouter):
    _payment_controller: PaymentControllerAdapter

    def __init__(self):
        super().__init__(Blueprint("payment", __name__, url_prefix=PaymentRoutes.BASE_URL))
        self.resolve_dependencies()

        @self.blueprint.route("/my-cards", methods=["GET"])
        @login_required
        def my_cards():
            response = self._payment_controller.find_user_cards(session["user"].id)
            return render_template("payments.html", cards=response.data)

        @self.blueprint.route("/add-card", methods=["GET", "POST"])
        @login_required
        def add_payment():

            if request.method == "POST":
                response = self._payment_controller.add_card(RequestDTO(request.form), session["user"].id)
                if not response.success:
                    flash(response.message, "error")
                    return redirect(request.referrer)

                flash("Card added successfully!", "success")
                return redirect(request.referrer)

            return render_template("add_payment.html")

    def resolve_dependencies(self):
        repository = CardRepositoryImpl()
        user_repository = UserRepositoryImpl()
        service = PaymentService(repository, user_repository)
        self._payment_controller = PaymentControllerAdapter(service)
from flask import Blueprint, session, render_template, request, url_for

from adapters.payment.payment_controller import PaymentControllerAdapter
from application.payment.usecases.payment_service import PaymentService
from infrastructure.db.sqlite3.repositories.card_repository import CardRepositoryImpl
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
            return render_template("payments.html", cards=response.data, referrer=request.referrer or url_for("index.index"))

    def resolve_dependencies(self):
        repository = CardRepositoryImpl()
        service = PaymentService(repository)
        self._payment_controller = PaymentControllerAdapter(service)
from flask import Blueprint, session, render_template, request, redirect, flash, url_for

from infrastructure.flask.decorators.login_required import login_required
from di.container import Container
from infrastructure.flask.routes.base_router import BaseRouter
from infrastructure.flask.routes.payment.routes_constants import PaymentRoutes
from presentation.dtos.request_dto import RequestDTO
from presentation.payment.payment_controller import PaymentController


class PaymentRouter(BaseRouter):
    _payment_controller: PaymentController

    def __init__(self, container: Container):
        super().__init__(Blueprint("payments", __name__, url_prefix=PaymentRoutes.BASE_URL), container)
        self._payment_controller = container.get(PaymentController)

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

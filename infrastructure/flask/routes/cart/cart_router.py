from flask import Blueprint, request, render_template, flash, redirect, url_for, session

from domain.payment.enums.payment_method import PaymentMethod
from infrastructure.flask.adapters.cart_session_adapter import CartSessionAdapter
from infrastructure.flask.decorators.login_required import login_required
from di.container import Container
from infrastructure.flask.routes.base_router import BaseRouter
from infrastructure.flask.routes.cart.routes_constants import CartRoutes
from presentation.cart.cart_web_service import CartWebService
from presentation.payment.dtos.payment_request_dto import PaymentRequestDTO
from presentation.payment.payment_controller import PaymentController


class CartRouter(BaseRouter):
    _payment_controller: PaymentController
    _cart_web_service: CartWebService
    _cart_session: CartSessionAdapter

    def __init__(self, container: Container):
        super().__init__(Blueprint("cart", __name__, url_prefix=CartRoutes.BASE_URL), container)
        self._payment_controller = container.get(PaymentController)
        self._cart_web_service = container.get(CartWebService)
        self._cart_session = container.get(CartSessionAdapter)

        @self.blueprint.route("/", methods=["GET", "POST"])
        def cart():
            user_cart = self._cart_session.get_cart()

            if request.method == "POST":
                machine_id = request.form.get("machine_id")
                cycle_id = request.form.get("price_id")

                if not user_cart.add_item(int(machine_id), int(cycle_id)):
                    flash("Este produto já está no seu carrinho!", "warning")
                    return redirect(request.referrer)

                self._cart_session.save_cart(user_cart)
                flash("Produto adicionado ao carrinho!", "success")
                return redirect(request.referrer)

            return render_template("cart.html", cart=self._cart_web_service.get_cart(user_cart))

        @self.blueprint.route(CartRoutes.REMOVE_ITEM, methods=["POST"])
        def remove_item():
            if not request.form.get("cycle_id") and not request.form.get("machine_id"):
                return redirect(url_for('index.cart.cart'))

            user_cart = self._cart_session.get_cart()
            user_cart.remove_item(int(request.form.get("machine_id")), int(request.form.get("cycle_id")))

            self._cart_session.save_cart(user_cart)

            flash("Produto removido do carrinho!", "success")
            return redirect(url_for("index.cart.cart"))

        @self.blueprint.route(CartRoutes.PAYMENT, methods=["GET", "POST"])
        @login_required
        def payment():
            user_cart = self._cart_session.get_cart()
            if request.method == "POST":
                dto = PaymentRequestDTO(
                    user_id=session["user"].id,
                    method=PaymentMethod(request.form.get("payment_method")),
                    card_id=request.form.get("card_id")
                )

                response = self._payment_controller.process_payment(dto, user_cart)
                if not response.success:
                    flash(response.message, "danger")
                    return redirect(url_for("index.cart.payment"))

                self._cart_session.clear_cart()
                flash("Pagamento realizado com sucesso!", "success")
                return redirect(url_for("index.index"))

            cart = self._cart_web_service.get_cart(user_cart)
            payment_info = {
                "products": cart.get_formatted_total(),
                "total": cart.get_formatted_total_with_discounts(),
                "discounts_as_text": cart.get_formatted_discounts(),
                "discounts": cart.discounts,
                "cards": self._payment_controller.find_user_cards(session["user"].id).data
            }

            return render_template("payment.html", cart=cart.items, payment_info=payment_info)

        @self.blueprint.route(CartRoutes.APPLY_DISCOUNT, methods=["POST"])
        @login_required
        def apply_discount():
            user_cart = self._cart_session.get_cart()
            ticket_code = request.form.get("ticket_code")

            if not ticket_code:
                flash("Código de desconto inválido!", "danger")
                return redirect(url_for("index.cart.payment"))

            try:
                user_cart.apply_discount(ticket_code, session["user"].id)
            except Exception as e:
                flash(str(e), "danger")
                return redirect(url_for("index.cart.payment"))

            self._cart_session.save_cart(user_cart)
            flash("Desconto aplicado com sucesso!", "success")
            return redirect(url_for("index.cart.payment"))

        @self.blueprint.route(CartRoutes.REMOVE_DISCOUNT, methods=["POST"])
        @login_required
        def remove_discount():
            user_cart = self._cart_session.get_cart()
            user_cart.remove_discount()
            self._cart_session.save_cart(user_cart)
            flash("Desconto removido com sucesso!", "success")
            return redirect(url_for("index.cart.payment"))

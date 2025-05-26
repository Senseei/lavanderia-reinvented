from flask import Blueprint, request, render_template, flash, redirect, url_for, session

from adapters.payment.dtos.payment_request_dto import PaymentRequestDTO
from adapters.payment.payment_controller import PaymentControllerAdapter
from application.machine.usecases.machine_service import MachineService
from application.payment.usecases.payment_service import PaymentService
from application.util.currency import br
from domain.payment.enums.payment_method import PaymentMethod
from infrastructure.db.sqlite3.repositories.card_repository import CardRepositoryImpl
from infrastructure.db.sqlite3.repositories.cycle_repository import CycleRepositoryImpl
from infrastructure.db.sqlite3.repositories.machine_repository import MachineRepositoryImpl
from infrastructure.db.sqlite3.repositories.user_repository import UserRepositoryImpl
from infrastructure.flask.adapters.cart_session_adapter import CartSessionAdapter
from infrastructure.flask.decorators.login_required import login_required
from infrastructure.flask.routes.base_router import BaseRouter
from infrastructure.flask.routes.cart.routes_constants import CartRoutes


class CartRouter(BaseRouter):
    _payment_controller: PaymentControllerAdapter

    def __init__(self):
        super().__init__(Blueprint("cart", __name__, url_prefix=CartRoutes.BASE_URL))
        self.resolve_dependencies()

        @self.blueprint.route("/", methods=["GET", "POST"])
        def cart():
            user_cart = CartSessionAdapter.get_cart()

            if request.method == "POST":
                machine_id = request.form.get("machine_id")
                cycle_id = request.form.get("price_id")

                if not user_cart.add_item(int(machine_id), int(cycle_id)):
                    flash("Este produto já está no seu carrinho!", "warning")
                    return redirect(request.referrer)

                CartSessionAdapter.save_cart(user_cart)
                flash("Produto adicionado ao carrinho!", "success")
                return redirect(request.referrer)

            return render_template("cart.html", cart=user_cart)

        @self.blueprint.route(CartRoutes.REMOVE_ITEM, methods=["POST"])
        def remove_item():
            if not request.form.get("cycle_id") and not request.form.get("machine_id"):
                return redirect(url_for('index.cart.cart'))

            user_cart = CartSessionAdapter.get_cart()
            user_cart.remove_item(int(request.form.get("machine_id")), int(request.form.get("cycle_id")))

            CartSessionAdapter.save_cart(user_cart)

            flash("Produto removido do carrinho!", "success")
            return redirect(url_for("index.cart.cart"))

        @self.blueprint.route(CartRoutes.PAYMENT, methods=["GET", "POST"])
        @login_required
        def payment():
            user_cart = CartSessionAdapter.get_cart()
            if request.method == "POST":
                dto = PaymentRequestDTO(
                    user_id=session["user"].id,
                    method=PaymentMethod(request.form.get("payment_method")),
                    cart_items= user_cart.get_items(),
                    total=user_cart.get_total_with_discounts(),
                    card_id=request.form.get("card_id")
                )

                response = self._payment_controller.process_payment(dto)
                if not response.success:
                    flash(response.message, "danger")
                    return redirect(url_for("index.cart.payment"))

                user_cart.clear()
                CartSessionAdapter.save_cart(user_cart)
                flash("Pagamento realizado com sucesso!", "success")
                return redirect(url_for("index.index"))

            payment_info = {
                "products": br(user_cart.get_total()),
                "total": br(user_cart.get_total_with_discounts()),
                "discounts": br(user_cart.get_discounts()),
                "cards": self._payment_controller.find_user_cards(session["user"].id).data
            }

            return render_template("payment.html", cart=user_cart.get_items(), payment_info=payment_info)

    def resolve_dependencies(self):
        repository = CardRepositoryImpl()
        user_repository = UserRepositoryImpl()
        cycle_repository = CycleRepositoryImpl()
        machine_repository = MachineRepositoryImpl()
        machine_service = MachineService(machine_repository, cycle_repository)
        service = PaymentService(repository, user_repository, machine_service)
        self._payment_controller = PaymentControllerAdapter(service)
from flask import Blueprint, request, render_template, flash, redirect, url_for, session

from infrastructure.flask.adapters.cart_session_adapter import CartSessionAdapter
from infrastructure.flask.routes.base_router import BaseRouter
from infrastructure.flask.routes.cart.routes_constants import CartRoutes


class CartRouter(BaseRouter):

    def __init__(self):
        super().__init__(Blueprint("cart", __name__, url_prefix=CartRoutes.BASE_URL))

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

    def resolve_dependencies(self):
        pass
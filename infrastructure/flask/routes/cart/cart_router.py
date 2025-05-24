from flask import Blueprint, request, render_template

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
                    return render_template("alert.html", message="This product is already in your cart!", path="/local")

                CartSessionAdapter.save_cart(user_cart)
                return render_template("alert.html", message="Added to your cart :)", path="/local")

            return render_template("cart.html", cart=user_cart)

    def resolve_dependencies(self):
        pass
from flask import Blueprint, render_template, session, redirect

from infrastructure.flask.routes.auth.auth_router import AuthRouter
from infrastructure.flask.routes.base_router import BaseRouter


class IndexRouter(BaseRouter):
    def __init__(self):
        super().__init__(Blueprint("index", __name__, url_prefix="/"))

        self.register_routes([
            AuthRouter().blueprint,
        ])

        @self.blueprint.route("/", methods=["GET"])
        def index():
            if not session.get("user_id"):
                return redirect("/login")

            # TODO: Implement the logic to fetch locations from the database
            return render_template("index.html", locations={})

    @classmethod
    def resolve_dependencies(cls):
        pass
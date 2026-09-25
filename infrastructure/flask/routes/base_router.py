from abc import ABC

from di.container import Container


class BaseRouter(ABC):
    def __init__(self, blueprint, container: Container):
        self.blueprint = blueprint
        self.container = container

    def register_routes(self, blueprints):
        for blueprint in blueprints:
            self.blueprint.register_blueprint(blueprint)

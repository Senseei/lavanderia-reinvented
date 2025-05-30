from abc import ABC, abstractmethod


class BaseRouter(ABC):
    def __init__(self, blueprint):
        self.blueprint = blueprint

    @abstractmethod
    def resolve_dependencies(self):
        """
        This method should be implemented in subclasses to resolve dependencies
        and return the controller instance.
        """
        pass

    def register_routes(self, blueprints):
        for blueprint in blueprints:
            self.blueprint.register_blueprint(blueprint)

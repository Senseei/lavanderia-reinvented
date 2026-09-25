import inspect
from typing import TypeVar, get_type_hints

from di.scanner import scan

T = TypeVar('T')


class DependencyError(Exception):
    """Base error for anything the container cannot resolve."""


class NoComponentError(DependencyError):
    pass


class AmbiguousComponentError(DependencyError):
    pass


class CircularDependencyError(DependencyError):
    pass


class Container:
    """
    Builds components on demand by reading their constructor type hints, like Spring's
    constructor injection. Every component is a singleton: built once, then cached.
    """

    def __init__(self, components: list[type]):
        self._components = list(components)
        self._instances: dict[type, object] = {}
        self._resolving: list[type] = []

    @classmethod
    def from_packages(cls, *packages: str) -> 'Container':
        return cls(scan(*packages))

    def get(self, requested: type[T]) -> T:
        implementation = self._find_implementation(requested)

        if implementation in self._instances:
            return self._instances[implementation]

        if implementation in self._resolving:
            path = " -> ".join(c.__name__ for c in [*self._resolving, implementation])
            raise CircularDependencyError(f"Circular dependency: {path}")

        self._resolving.append(implementation)
        try:
            instance = implementation(**self._resolve_arguments(implementation))
        finally:
            self._resolving.pop()

        self._instances[implementation] = instance
        return instance

    def _find_implementation(self, requested: type) -> type:
        """
        A component satisfies a request for itself or for any class it extends,
        which is how an interface (UnitRepository) is bound to its implementation (UnitRepositoryImpl).
        """
        if not isinstance(requested, type):
            raise DependencyError(f"Cannot inject {requested!r}: only plain classes are supported")

        candidates = [c for c in self._components if issubclass(c, requested)]

        if requested in candidates:
            return requested
        if not candidates:
            required_by = f" (required by {self._resolving[-1].__name__})" if self._resolving else ""
            raise NoComponentError(f"No component found for {requested.__name__}{required_by}. Is it decorated with @component and scanned?")
        if len(candidates) > 1:
            names = ", ".join(c.__name__ for c in candidates)
            raise AmbiguousComponentError(f"More than one component implements {requested.__name__}: {names}")

        return candidates[0]

    def _resolve_arguments(self, cls: type) -> dict[str, object]:
        if cls.__init__ is object.__init__:
            return {}

        hints = get_type_hints(cls.__init__)
        arguments = {}

        for name, parameter in inspect.signature(cls.__init__).parameters.items():
            if name == "self" or parameter.kind in (parameter.VAR_POSITIONAL, parameter.VAR_KEYWORD):
                continue

            has_default = parameter.default is not parameter.empty

            if name not in hints:
                if has_default:
                    continue
                raise DependencyError(f"{cls.__name__}.__init__ parameter '{name}' has no type hint, so it cannot be injected")

            try:
                arguments[name] = self.get(hints[name])
            except NoComponentError:
                # Nothing registered for an optional parameter: keep its default instead of failing
                if not has_default:
                    raise

        return arguments

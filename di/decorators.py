from typing import TypeVar

T = TypeVar('T', bound=type)

COMPONENT_MARKER = "__di_component__"

_components: list[type] = []


def component(cls: T) -> T:
    """
    Marks a class as a component managed by the container, like Spring's @Component.
    The class is registered when its module is imported, so it must be reached by the scanner.
    """
    if not isinstance(cls, type):
        raise TypeError(f"@component can only decorate classes, got {cls!r}")

    # Checks __dict__, not getattr: a subclass inherits the attribute but is not a component by itself
    if COMPONENT_MARKER not in cls.__dict__:
        setattr(cls, COMPONENT_MARKER, True)
        _components.append(cls)

    return cls


def is_component(cls: type) -> bool:
    return COMPONENT_MARKER in cls.__dict__


def registered_components() -> list[type]:
    return list(_components)

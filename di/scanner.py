import importlib
import importlib.util
from pathlib import Path

from di.decorators import registered_components


def scan(*packages: str) -> list[type]:
    """
    Imports every module under the given packages so their @component decorators run,
    then returns the components that belong to those packages.
    Works with folders without __init__.py, which pkgutil.walk_packages skips.
    """
    for package in packages:
        for module_name in _find_modules(package):
            importlib.import_module(module_name)

    return [cls for cls in registered_components() if _belongs_to(cls.__module__, packages)]


def _find_modules(package: str) -> list[str]:
    spec = importlib.util.find_spec(package)
    if spec is None or spec.submodule_search_locations is None:
        raise ValueError(f"'{package}' is not an importable package")

    modules = []
    for location in spec.submodule_search_locations:
        root = Path(location)
        for file in sorted(root.rglob("*.py")):
            if "__pycache__" in file.parts:
                continue

            # application/unit/usecases/unit_service.py -> application.unit.usecases.unit_service
            parts = file.relative_to(root).with_suffix("").parts
            if parts[-1] == "__init__":
                parts = parts[:-1]
            modules.append(".".join((package, *parts)))

    return modules


def _belongs_to(module_name: str, packages: tuple[str, ...]) -> bool:
    return any(module_name == package or module_name.startswith(package + ".") for package in packages)

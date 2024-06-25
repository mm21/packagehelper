"""
Utilities for inspecting packages and modules.
"""

from types import ModuleType

__all__ = [
    "get_package",
    "get_package_path",
    "is_package",
]


def get_package(module: ModuleType) -> ModuleType:
    """
    Get containing package, or the input module itself if it is a package.
    """

    if is_package(module):
        return module
    else:
        return module.__package__


def get_package_path(module: ModuleType) -> str:
    """
    Get string path to containing package, or to the input module itself if it
    is specifically a package.

    Examples:

    my_package.my_subpackage -> "my_package.my_subpackage"
    my_package.my_subpackage.my_submodule -> "my_package.my_subpackage"
    """

    # assume module is package
    package_path: list[str] = module.__name__.split(".")

    if not is_package(module):
        # have a module, we want a package
        assert len(package_path) > 1
        del package_path[-1]

    return ".".join(package_path)


def is_package(module: ModuleType) -> bool:
    """
    Returns True if the provided module is a package specifically.

    ```{note}
    In Python, all packages are modules but not all modules are packages.
    This API determines the latter case -- whether the module is
    specifically a package.
    ```
    """
    try:
        module.__module__
    except AttributeError:
        # have a package
        return True

    # have a module which is not a package
    return False

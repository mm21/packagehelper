"""
Utilities for accessing resources from packages.
"""

from importlib.resources.abc import Traversable
from pathlib import Path
from types import ModuleType
import importlib
import os


from .packages import get_package

__all__ = [
    "get_resource",
]


def get_resource(
    from_module: ModuleType, rel_path: str, use_import: bool | None = None
) -> Path:
    """
    Take path to resource relative to containing package, and return a Path
    object to its content as a file on the local filesystem.

    `rel_path` should not include a leading `/`.

    You might want to pass your project's package itself as the
    module. This gives you access to all resources relative to your project's
    root. Resources may be extracted from subpackages as well.
    """

    resource: Path

    # normalize to package
    from_package: ModuleType = get_package(from_module)

    # split relative path using directory separator
    rel_path_split: list[str] = rel_path.split("/")

    # invoke correct function to get resource based on input
    resource = {
        True: _get_from_import,
        False: _get_from_file,
        None: _get_from_any,
    }[use_import](from_package, rel_path_split)

    assert resource.is_file

    return resource


def _get_from_import(
    from_package: ModuleType, rel_path_split: list[str]
) -> Path:
    """
    Get path to file by extracting the resource from an installed package.
    """

    resource: Path

    # get package
    package_trav: Traversable = importlib.resources.files(from_package)

    # get resource from package
    resource_trav: Traversable = package_trav.joinpath(*rel_path_split)

    # get resource as file
    with importlib.resources.as_file(resource_trav) as path:
        resource = path

    return resource


def _get_from_file(from_package: ModuleType, rel_path_split: list[str]) -> Path:
    """
    Get path to file by checking file location of the provided module.
    """

    resource: Path

    folder_path: Path = Path(from_package.__file__).parent
    resource = folder_path / os.path.join(*rel_path_split)

    assert resource.is_file()

    return resource


def _get_from_any(from_package: ModuleType, rel_path_split: list[str]) -> Path:
    """
    Try both approaches. Raises exception if neither approaches worked.
    """

    try:
        return _get_from_import(from_package, rel_path_split)
    except ModuleNotFoundError:
        pass

    try:
        return _get_from_file(from_package, rel_path_split)
    except AssertionError:
        pass

    raise Exception(
        f"Unable to find resource: from_package={from_package}, rel_path={rel_path_split}"
    )

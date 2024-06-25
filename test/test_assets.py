"""
Tests for extracting assets, either from an installed package or the local
filesystem.
"""

from pathlib import Path

from packagehelper import get_resource
import packagehelper

IMPORT_TEXT = "Hello, world import #{num}!"
FILE_TEXT = "Hello, world file #{num}!"


def test_import():
    """
    Test resources from installed package.
    """

    test1_path: Path
    test2_path: Path

    test1_path = get_resource(
        packagehelper, "_test_assets/test1.txt", use_import=True
    )
    test2_path = get_resource(
        packagehelper, "_test_assets/test2/test2.txt", use_import=True
    )

    test1: str = test1_path.read_text()
    test2: str = test2_path.read_text()

    assert test1 == IMPORT_TEXT.format(num=1)
    assert test2 == IMPORT_TEXT.format(num=2)


def test_file(request):
    """
    Test resources from local filesystem.
    """

    test1_path: Path
    test2_path: Path

    test1_path = get_resource(
        request.module, "assets/test1.txt", use_import=False
    )
    test2_path = get_resource(
        request.module, "assets/test2/test2.txt", use_import=False
    )

    test1: str = test1_path.read_text()
    test2: str = test2_path.read_text()

    assert test1 == FILE_TEXT.format(num=1)
    assert test2 == FILE_TEXT.format(num=2)


def test_any(request):

    test1_path: Path
    test2_path: Path

    test1_path = get_resource(packagehelper, "_test_assets/test1.txt")
    test2_path = get_resource(request.module, "assets/test2/test2.txt")

    test1: str = test1_path.read_text()
    test2: str = test2_path.read_text()

    assert test1 == IMPORT_TEXT.format(num=1)
    assert test2 == FILE_TEXT.format(num=2)

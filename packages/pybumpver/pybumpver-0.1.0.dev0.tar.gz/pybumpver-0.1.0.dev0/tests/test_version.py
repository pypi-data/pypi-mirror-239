from __future__ import annotations

from pybumpver import __version__


def test_version():
    assert __version__ == "0.1.0dev0"

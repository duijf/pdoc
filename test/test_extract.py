import sys
from pathlib import Path

import pytest

from pdoc.extract import parse_specs, module_mtime, parse_spec

here = Path(__file__).parent


def test_parse_specs():
    assert list(parse_specs(["dataclasses"])) == ["dataclasses"]
    with pytest.raises(ValueError, match="Module not found"):
        with pytest.warns(RuntimeWarning, match="Cannot find spec for unknown"):
            assert parse_specs(["unknown"])
    with pytest.warns(RuntimeWarning, match="Cannot find spec for unknown"):
        assert list(parse_specs(["dataclasses", "unknown"])) == ["dataclasses"]

    with pytest.warns(RuntimeWarning, match="Error importing subpackage"):
        assert list(parse_specs([here / "import_err"])) == [
            "test.import_err",
            "test.import_err.err",
        ]
    with pytest.raises(ValueError, match="Module not found"):
        assert parse_specs([])


def test_parse_spec():
    p = sys.path

    assert parse_spec("dataclasses") == "dataclasses"
    assert sys.path == p

    assert parse_spec(here / "testdata" / "demo.py") == "demo"
    assert str(here / "testdata") in sys.path
    sys.path = p

    assert (
        parse_spec(here / "testdata" / "demopackage" / "_child.py")
        == "demopackage._child"
    )
    assert str(here / "testdata") in sys.path
    sys.path = p


def test_module_mtime():
    assert module_mtime("dataclasses")
    assert module_mtime("unknown") is None
    assert module_mtime("dataclasses.abc") is None

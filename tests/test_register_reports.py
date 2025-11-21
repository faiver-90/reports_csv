import types
from unittest.mock import patch

import pytest

from src.reports.register_reports import _auto_register, register


@pytest.fixture
def clear_register():
    register.clear()
    yield
    register.clear()


@pytest.mark.parametrize(
    "meta,expected_len",
    [
        ({"name": "r1", "func": lambda x: x, "headers": []}, 1),
        ({"name": "abc", "func": lambda x: x, "headers": ["h"]}, 1),
        (None, 0),
    ],
)
def test_autoload_meta_variants(meta, expected_len, clear_register):
    fake_module = (
        types.SimpleNamespace(__report__=meta) if meta else types.SimpleNamespace()
    )
    fake_iter = [types.SimpleNamespace(name="m")]

    with patch(
        "src.reports.register_reports.pkgutil.iter_modules", return_value=fake_iter
    ):
        with patch(
            "src.reports.register_reports.importlib.import_module",
            return_value=fake_module,
        ):
            _auto_register()

    assert len(register) == expected_len

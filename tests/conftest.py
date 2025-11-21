from unittest.mock import patch

import pytest


@pytest.fixture
def patch_register():
    """Фикстура для подмены реестра отчётов."""
    with patch("src.parse_args.register", {"perf": {}, "avg": {}}):
        yield


@pytest.fixture
def sample_rows_valid():
    return [
        {"position": "Dev", "performance": "10"},
        {"position": "Dev", "performance": "20"},
        {"position": "QA", "performance": "5"},
    ]


@pytest.fixture
def sample_rows_invalid():
    return [
        {"position": "Dev", "performance": "10"},
        {"position": "Dev", "performance": "bad"},
        {"position": None, "performance": "20"},
        {"performance": "5"},
    ]

from unittest.mock import patch

import pytest

from src.parse_args import parse_args


@pytest.mark.parametrize(
    "argv,register,expected",
    [
        (
            ["--files", "a.csv", "--report", "r1"],
            {"r1": {}, "r2": {}},
            (["a.csv"], "r1"),
        ),
        (
            ["--files", "x.csv", "y.csv", "--report", "r2"],
            {"r1": {}, "r2": {}},
            (["x.csv", "y.csv"], "r2"),
        ),
        (
            ["--files", "file.csv", "--report", "big"],
            {"big": {}},
            (["file.csv"], "big"),
        ),
    ],
)
def test_parse_args_success(argv, register, expected):
    with patch("src.parse_args.register", register):
        args = parse_args(argv)
        assert args.files == expected[0]
        assert args.report == expected[1]


@pytest.mark.parametrize(
    "argv",
    [
        ["--files", "a.csv"],
        ["--report", "r1"],
        [],
        ["--files"],
    ],
)
def test_parse_args_fail(argv):
    with patch("src.parse_args.register", {"r1": {}}):
        with pytest.raises(SystemExit):
            parse_args(argv)

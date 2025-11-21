import pytest

from src.reports.base import BaseReport


class Dummy1(BaseReport):
    name = "d1"
    headers = ["a"]

    def process(self, rows):
        return [("x", 1)]


class Dummy2(BaseReport):
    name = "d2"
    headers = ["a", "b"]

    def process(self, rows):
        return [("y", 2)]


@pytest.mark.parametrize(
    "report_cls,expected",
    [
        (Dummy1, ("d1", ["a"], ("x", 1))),
        (Dummy2, ("d2", ["a", "b"], ("y", 2))),
    ],
)
def test_base_report_variants(report_cls, expected):
    r = report_cls()
    meta = r.__report__
    assert meta["name"] == expected[0]
    assert meta["headers"] == expected[1]
    assert r.process([])[0] == expected[2]

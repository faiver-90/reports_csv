import pytest

from src.reports.type_reports.performance import PerformanceReport, PerformanceResult


@pytest.fixture
def report():
    return PerformanceReport()


@pytest.mark.parametrize(
    "rows,expected",
    [
        ([], []),
        (
            [{"position": "Dev", "performance": "10"}],
            [("Dev", 10.0)],
        ),
        (
            [
                {"position": "Dev", "performance": "10"},
                {"position": "Dev", "performance": "20"},
                {"position": "QA", "performance": "5"},
            ],
            [("Dev", 15.0), ("QA", 5.0)],
        ),
        (
            [
                {"position": "Dev", "performance": "10"},
                {"position": "Dev", "performance": "bad"},
                {"position": None, "performance": "20"},
                {"performance": "5"},
            ],
            [("Dev", 10.0)],
        ),
    ],
)
def test_process_variants(report, rows, expected):
    assert report.process(rows) == expected


def test_dataclass():
    obj = PerformanceResult(position="Dev", avg_performance=12.5)
    assert obj.position == "Dev"
    assert obj.avg_performance == 12.5

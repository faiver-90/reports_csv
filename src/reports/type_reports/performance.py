from collections import defaultdict
from dataclasses import dataclass

from src.reports.base import BaseReport


@dataclass(slots=True)
class PerformanceResult:
    """DTO результата по средней производительности позиции."""

    position: str
    avg_performance: float


class PerformanceReport(BaseReport):
    name = "performance"
    headers = ["position", "avg_performance"]

    def process(self, rows: list[dict[str, str]]):
        sums = defaultdict(float)
        counts = defaultdict(int)

        for row in rows:
            pos = row.get("position")
            val = row.get("performance")
            if pos is None or val is None:
                continue
            try:
                perf = float(val)
            except (TypeError, ValueError):
                continue

            sums[pos] += perf
            counts[pos] += 1

        results: list[PerformanceResult] = []
        for pos, total in sums.items():
            avg = total / counts[pos]
            results.append(PerformanceResult(pos, avg))

        results.sort(key=lambda r: r.avg_performance, reverse=True)
        return [(r.position, r.avg_performance) for r in results]


report = PerformanceReport()
__report__ = report.__report__

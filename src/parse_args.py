import argparse
import logging

from src.reports.register_reports import register

logger = logging.getLogger(__name__)


def parse_args(argv: list[str]) -> argparse.Namespace:
    reports_list = "\n".join(f"  {name}" for name in register.items())

    p = argparse.ArgumentParser(
        prog="ratings",
        description=(
            "Rating aggregation and report generation from CSV.\n"
            "Available reports:\n"
            f"{reports_list}"
        ),
    )
    p.add_argument("--files", nargs="+", required=True, help="Paths to CSV files.")
    p.add_argument(
        "--report",
        required=True,
        choices=list(register.keys()),
        help="Report Title.",
    )
    known, unknown = p.parse_known_args(argv)

    if unknown:
        logger.error(f"Ignoring unknown args: {' '.join(unknown)}")

    return known

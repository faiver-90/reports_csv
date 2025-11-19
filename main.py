import logging
import sys

import tabulate  # type: ignore

from src.log_conf import setup_logger
from src.parse_args import parse_args
from src.reports.io_operation import read_csv_files
from src.reports.register_reports import register

setup_logger()
logger = logging.getLogger(__name__)


def main(argv: list[str] | None = None) -> int:
    try:
        ns = parse_args(argv or sys.argv[1:])

        if not ns.files:
            logger.error("No input files")
            return 2

        meta = register.get(ns.report)
        if not meta or "func" not in meta or "headers" not in meta:
            logger.error(f"Report '{ns.report}' is misconfigured")
            return 2

        rows = read_csv_files(ns.files)
        if not rows:
            logger.error("No data rows after reading CSVs")

        try:
            final_rows = meta["func"](rows)  # type: ignore
        except KeyboardInterrupt:
            logger.error("Interrupted")
            return 130
        except Exception as e:
            logger.error(f"Report '{ns.report}' failed: {e}")
            return 1

        if final_rows:
            print(
                tabulate.tabulate(
                    final_rows,
                    headers=meta["headers"],
                    tablefmt="github",
                    floatfmt=".2f",
                )
            )
        else:
            logger.error("Nothing to print")
        return 0
    except Exception as e:
        logger.error(f"Unexpected: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

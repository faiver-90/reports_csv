import csv
import logging
from collections.abc import Iterable
from pathlib import Path

logger = logging.getLogger(__name__)


def _open_text(p: Path, mode: str = "r", encoding="utf-8") -> Iterable[str]:
    return p.open(mode, encoding=encoding, newline="")


def read_csv_files(files: Iterable[str], delimiter: str = ",") -> list[dict[str, str]]:
    rows: list[dict] = []
    for f_name in files:
        path = Path(f_name)
        if not path.exists():
            logger.error(f"File not found: {path}")
            continue
        try:
            with _open_text(path, "r", "utf-8") as f:  # type: ignore
                print(type(f))
                reader = csv.DictReader(f, delimiter=delimiter)
                for row in reader:
                    if not row:
                        continue
                    if any(v is None for v in row.values()):
                        logger.error(f"Bad CSV {path}: inconsistent columns")
                        return []  # весь файл считаем битым
                    rows.append(row)
        except FileNotFoundError:
            logger.error(f"File not found: {path}")
        except PermissionError as e:
            logger.error(f"No permission {path}: {e}")
        except UnicodeDecodeError as e:
            logger.error(f"Bad encoding {path}: {e}")
        except csv.Error as e:
            logger.error(f"Bad CSV {path}: {e}")

    return rows

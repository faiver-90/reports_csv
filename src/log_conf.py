import logging
from pathlib import Path


def setup_logger() -> None:
    Path("logs").mkdir(parents=True, exist_ok=True)

    root = logging.getLogger()
    root.setLevel(logging.ERROR)

    for h in list(root.handlers):
        root.removeHandler(h)
        try:
            h.close()
        except Exception:
            pass

    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    fh = logging.FileHandler("logs/app.log", mode="a", encoding="utf-8")
    fh.setFormatter(fmt)

    ch = logging.StreamHandler()
    ch.setFormatter(fmt)

    root.addHandler(fh)
    root.addHandler(ch)
    root.propagate = False

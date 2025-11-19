import importlib
import pkgutil
from pathlib import Path

REPORTS_PACKAGE = "src.reports.type_reports"

register = {}


def _auto_register():
    REPORTS_PACKAGE.replace(".", "/")
    pkg_path = Path(__file__).resolve().parent / "type_reports"

    for module_info in pkgutil.iter_modules([pkg_path]):
        module_name = module_info.name
        full_import_path = f"{REPORTS_PACKAGE}.{module_name}"

        module = importlib.import_module(full_import_path)

        meta = getattr(module, "__report__", None)

        if meta and "name" in meta:
            register[meta["name"]] = meta


_auto_register()

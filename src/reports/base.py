from abc import ABC, abstractmethod
from typing import Any


class BaseReport(ABC):
    """Базовый класс всех отчётов.
    Гарантирует наличие name, headers, process() и __report__.
    """

    name: str
    headers: list[str]

    @abstractmethod
    def process(self, rows: list[dict[str, str]]) -> list[tuple[str, Any]]: ...

    @property
    def __report__(self) -> dict[str, Any]:
        """Единая структура для всех отчётов."""
        return {
            "name": self.name,
            "func": self.process,
            "headers": self.headers,
        }

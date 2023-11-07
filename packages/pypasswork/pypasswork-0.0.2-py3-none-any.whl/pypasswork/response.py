from enum import Enum
from collections.abc import Mapping
from typing import Any, Literal, TypeAlias


PassworkData: TypeAlias = str | Mapping[str, Any] | list[Mapping[str, Any]]


class PassworkStatus(Enum):
    SUCCESS = 0
    FAILED = 1


class PassworkResponse:
    def __init__(self, status: Literal['success', 'failed'], data: PassworkData):
        self._status = status
        self._data = data

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(status={self.status.value}, data={self.data})'

    @property
    def status(self) -> PassworkStatus:
        return PassworkStatus[self._status.upper()]

    @property
    def data(self) -> PassworkData:
        return self._data

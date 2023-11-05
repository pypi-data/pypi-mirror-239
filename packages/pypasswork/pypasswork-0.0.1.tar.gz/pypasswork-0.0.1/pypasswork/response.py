from ast import Pass
from collections.abc import Mapping
from typing import Any, Literal, TypeAlias


PassworkData: TypeAlias = str | Mapping[str, Any] | list[Mapping[str, Any]]
 
class PassworkResponse:
    def __init__(self, status: Literal['success', 'failed'], data: PassworkData):
        self._status = status
        self._data = data

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(status={self._status}, data={self.data})'

    @property
    def status(self) -> int:
        return 1 if self._status == 'success' else 0

    @property
    def data(self) -> str | Mapping[str, Any] | list[Mapping[str, Any]]:
        return self._data

"""PassworkAPI folders operations api"""

from collections.abc import Sequence
import dataclasses
from dataclasses import dataclass
from typing import Any, Optional

from pypasswork.operations.passwords import Password


@dataclass
class Folder:
    vault_id: str
    id: str
    name: str
    parent_id: Optional[str]

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(id={self.id}, name={self.name})'

    def as_dict(self) -> dict[str, Any]:
        return dataclasses.asdict(self)


class Folders:
    """Implement Passwork folders API"""

    def __init__(self, api):
        self._api = api

    def search(self) -> Sequence[Folder]: ...

    def get(self) -> Folder: ...

    def passwords(self) -> Sequence[Password]: ...

"""Password Vaults operations"""

import dataclasses
import logging
from collections.abc import Sequence, Mapping
from dataclasses import dataclass
from typing import Any, Optional

from pypasswork.exceptions import PassworkInteractionError
from pypasswork.operations.folders import Folder
from pypasswork.response import PassworkResponse, PassworkStatus


logger = logging.getLogger(__name__)


@dataclass
class Vault:
    id: str
    name: str
    access: str
    scope: str
    visible: Optional[bool]
    folders_amount: int
    passwords_amount: int

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(id={self.id}, name={self.name})'

    def as_dict(self) -> Mapping[str, Any]:
        return dataclasses.asdict(self)


class Vaults:
    """
    Implement operations with Passwork vaults:
    - list
    - folders
    ...
    """

    def __init__(self, api):
        self._api = api

    def list_vaults(self) -> Sequence[Vault]:
        """
        Get all available vaults

        Returns:
            a list of Vault objects
        """

        logger.debug('In list')

        resp: PassworkResponse = self._api.req('GET', endpoint='vaults/list', timeout=10)
        if resp.status is not PassworkStatus.SUCCESS:
            raise PassworkInteractionError(f'Cannot get list of vaults: {resp}')

        vaults = []
        for vault in resp.data:
            try:
                vaults.append(
                    Vault(
                        id=vault['id'],
                        name=vault['name'],
                        access=vault['access'],
                        scope=vault['scope'],
                        visible=vault['visible'] if vault.get('visible') else None,
                        folders_amount=vault['foldersAmount'],
                        passwords_amount=vault['passwordsAmount']
                    )
                )
            except KeyError as e:
                raise PassworkInteractionError(f'Cannot prepare Vault() object from: "{vault}": missing key {e}')

        return vaults

    def get(self) -> Vault: ...

    def folders(self, vault_id: str | Vault) -> Sequence[Folder]:
        """
        Get all vault folders

        Returns:
            a list of Folder object in given Vault
        """

        logger.debug('In folders')

        vault_id = vault_id.id if isinstance(vault_id, Vault) else vault_id
        resp: PassworkResponse = self._api.req('GET', endpoint=f'/vaults/{vault_id}/folders')

        folders = []
        for folder in resp.data:
            try:
                folders.append(
                    Folder(
                        vault_id=folder['vaultId'],
                        id=folder['id'],
                        name=folder['name'],
                        parent_id=folder['parentId'] if folder.get('parentId') else None
                    )
                )
            except KeyError as e:
                raise PassworkInteractionError(f'Cannot prepare Folder() object from: "{folder}": missing key {e}')

        return folders

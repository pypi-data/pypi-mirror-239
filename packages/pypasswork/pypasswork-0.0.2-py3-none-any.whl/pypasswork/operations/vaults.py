"""Password Vaults operations"""

from dataclasses import dataclass
import logging
from typing import Optional


logger = logging.getLogger(__name__)

@dataclass
class Vault:
    id: str
    name: str

class Vaults:
    def __init__(self, api) -> Optional[list[Vault]]:
        self._api = api

    def list(self) -> Optional[str]:
        """
        Search vaults in Passwork and return ID of given Vault name

        Parameters:
            name: target vault name
        Returns:
            VaultId as a string or None if vault name not provided
        """

        logger.debug('In _get_vault_id')

        if not self.name:
            return None

        resp = self._api._make_request('GET', endpoint='/vaults/list', timeout=10)

        return [Vault(vault['id'], vault['name']) for vault in resp.data]

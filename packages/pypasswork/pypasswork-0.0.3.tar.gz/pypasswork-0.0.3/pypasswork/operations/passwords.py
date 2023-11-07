"""Passwork API /passwords endpoint operations"""

import base64
from collections.abc import Sequence
import dataclasses
import logging
from dataclasses import dataclass
from typing import Optional

from pypasswork.exceptions import PassworkInteractionError
from pypasswork.response import PassworkResponse, PassworkStatus


logger = logging.getLogger(__name__)


@dataclass
class Password:
    vault_id: str
    id: str
    name: str
    login: str
    description: str
    encrypted_password: str
    url: str
    attachments: list[dict]
    color: int
    tags: list[str]
    path: list[dict]
    is_favorite: bool
    access: str
    access_code: int

    def __repr__(self) -> str:
        return f'Password(name={self.name})'

    @property
    def password(self) -> str:
        """Returns decrypted password string"""

        return base64.b64decode(self.encrypted_password).decode('utf-8')

    def as_dict(self) -> dict:
        return dataclasses.asdict(self)


class Passwords:
    def __init__(self, api) -> None:
        self._api = api

    def search(self,
               query: str,
               vault_id: Optional[str] = None,
               colors: Optional[list[int]] = None,
               tags: Optional[list[str]] = None,
               include_shared: bool = False,
               exact: bool = False,
               exact_tags: bool = False) -> Optional[Sequence[Password]]:
        """
        Implement search password in Passwork with given entry name.

        Args:
            query: password name to search by
            vault_id: optional vault_id to search within
            colors: colors id to filter passwords
            tags: tags name to filter passwords
            include_shared: switch if shared password must be included in search result
            exact: return only password exactly match given query
            exact_tags: return only password has all given tags
        Returns:
            a list of password matched with query as Password instance
        """

        logger.debug('In search')

        search_params = {'query': query}
        if vault_id:
            search_params['vaultId'] = vault_id
        if colors:
            search_params['colors'] = colors
        if tags:
            search_params['tags'] = tags
        if include_shared:
            search_params['includeShared'] = include_shared

        resp = self._api.req('POST', endpoint='passwords/search', parameters=search_params, timeout=10)
        passwords = [self.get(password['id']) for password in resp.data]

        if exact:
            passwords = [password for password in passwords if password.name == query]
        if exact_tags:
            passwords = [password for password in passwords if set(password.tags) == set(tags)]

        return passwords

    def get(self, password_id: str) -> Optional[Password]:
        """
        Retrieve password information by ID

        Args:
            password_id: passwork id to get from Passwork
        Returns:
            Password as a string
        Raises:
            PassworkInteractionError
        """

        logger.debug('In get')

        try:
            resp: PassworkResponse = self._api.req('GET', endpoint=f'passwords/{password_id}')
        except PassworkInteractionError as e:
            logger.error(f'Cannot get password wih ID "{password_id}": {e}')
        else:
            if resp.status is not PassworkStatus.SUCCESS:
                return None

            pw = resp.data
            return Password(
                vault_id=pw['vaultId'],
                id=pw['id'],
                name=pw['name'],
                login=pw['login'],
                description=pw['description'],
                encrypted_password=pw['cryptedPassword'],
                url=pw['url'],
                attachments=pw['attachments'],
                color=pw['color'],
                tags=pw['tags'],
                path=pw['path'],
                is_favorite=pw['isFavorite'],
                access=pw['access'],
                access_code=pw['accessCode']
            )

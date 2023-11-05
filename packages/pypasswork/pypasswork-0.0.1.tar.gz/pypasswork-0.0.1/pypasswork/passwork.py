import base64
import logging
from socket import gaierror
from typing import Optional

from requests import Request, Session
from requests.exceptions import ConnectionError, ConnectTimeout, JSONDecodeError

from pypasswork.exceptions import PassworkInteractionError
from pypasswork.response import PassworkResponse

logger = logging.getLogger(__name__)


class PassworkAPI:
    """
    PassworkAPI class to interract with Passwork API.
    Parameters:
        url: URl to connect to API (e.g: https://passwork.me)
        key: API key to authorize with
        vault_name: name of Passwork API to work with

    Returns:
        PassworkResponse instance
    Raises:
        PassworkInteractionError
    """

    def __init__(self, url: str, key: str, vault_name: Optional[str] = None):
        self._url = url
        self._key = key
        self._session = Session()
        self._vault_name = vault_name
        self.__token = None
        self._vault_id = None

        self.__token = self._login()
        self._vault_id = self._get_vault_id()
        
    def __repr__(self) -> str:
        return f'PassworkAPI(url={self._url}, vault={self._vault_name})'

    @property
    def _headers(self) -> dict[str, str]:
        if self.__token:
            return {'Passwork-Auth': self.__token, 'Content-Type': 'application/json'}
        else:
            return {}

    def _make_request(self,
                      method: str,
                      endpoint: str,
                      parameters: dict[str, str] | None = None,
                      timeout: int = 5
                      ) -> PassworkResponse:
        """
        Make base request to PassworkAPI and return result

        Args:
            method: http method, supported by PassworkAPI (GET, POST, PUT, DELETE)
            endpoint: Passwork method endpoint
            parameters: data payload parameters as JSON
            timeout: total timeout while we wait API response
        Returns:
            Instance of PassworkResponse
        Raises:
            PassworkInteractionError
        """

        base_url = f'{self._url}/api/v4{endpoint}'

        pw_req = Request(method=method, url=base_url, headers=self._headers, json=parameters).prepare()

        try:
            with self._session as s:
                logger.debug(f'PassworkAPI request: ({pw_req.method}) headers={self._headers}, url={pw_req.url}')
                resp = s.send(request=pw_req, timeout=timeout)
        except (gaierror, ConnectionError, ConnectTimeout) as e:
            raise PassworkInteractionError(f'Passwork API operations failed: {e}')

        if not resp.status_code == 200:
            raise PassworkInteractionError(f'Passwork API error: code={resp.status_code}: {resp.text}')

        try:
            data = resp.json()
        except JSONDecodeError as e:
            logger.debug(f'Raw PassworkAPI response: {resp.text}')
            raise PassworkInteractionError(f'Passwork response is not a valid JSON document: {e}')

        return PassworkResponse(status=data['status'], data=data['data'])

    def _login(self) -> str:
        """
        Login to Passwork API with given key and get auth token string.

        Returns:
            Passwork API token
        """

        logger.debug('In _login')

        try:
            resp = self._make_request('POST', endpoint=f'/auth/login/{self._key}')
        except PassworkInteractionError as e:
            raise PassworkInteractionError(f'Passwork login failed: {e}')

        return resp.data['token']

    def _logout(self) -> None:
        """
        Logout from Passwork"""

        logger.debug('In _logout')

        self._make_request('POST', endpoint='/auth/logout')

    def _get_vault_id(self) -> Optional[str]:
        """
        Search vaults in Passwork and return ID of given Vault name

        Returns:
            VaultId as a string or None if vault name not provided
        """

        logger.debug('In _get_vault_id')

        if not self._vault_name:
            return None

        resp = self._make_request('GET', endpoint='/vaults/list', timeout=10)

        # FIXME: check KeyError
        for vault in resp.data:
            if vault['name'] == self._vault_name:
                return vault['id']
        else:
            raise PassworkInteractionError(f'Cannot find vault_id for given vault name: "{self._vault_name}"')

    def search_password(self, password_name: str) -> Optional[str]:
        """
        Implement search password in Passwork with given entry name.

        Args:
            password_name: Passwork password name to search

        Returns:
            Passwork as a string
        """

        logger.debug('In search_password')

        search_params = {'query': password_name}
        if self._vault_id:
            search_params['vaultId'] = self._vault_id

        resp = self._make_request('POST', endpoint='/passwords/search', parameters=search_params, timeout=10)

        for password in resp.data:
            if password['name'] == password_name:
                return self._get_password(password['id'])
        else:
            logger.debug(f'Cannot find passwork with name: "{password_name}"')
            return None

    def _get_password(self, password_id: str) -> Optional[str]:
        """
        Retrieve password information by ID

        Args:
            password_id: passwork id to get from Passwork
        Returns:
            Password as a string
        Raises:
            PassworkInteractionError
        """

        logger.debug('In _get_password')

        try:
            resp = self._make_request('GET', endpoint=f'/passwords/{password_id}')
        except PassworkInteractionError as e:
            logger.error(f'Cannot get password wih ID "{password_id}": {e}')
        else:
            password = base64.b64decode(resp.data["cryptedPassword"]).decode('utf-8')
            return password

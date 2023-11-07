import logging
from socket import gaierror

from requests import Request, Session
from requests.exceptions import ConnectionError, ConnectTimeout, JSONDecodeError

from pypasswork.exceptions import PassworkInteractionError
from pypasswork.response import PassworkResponse
from pypasswork.operations.passwords import Passwords


logger = logging.getLogger(__name__)


class PassworkAPI:
    """
    PassworkAPI class to interract with Passwork API.
    Parameters:
        url: URl to connect to API (e.g: https://passwork.me)
        key: API key to authorize with
    Returns:
        PassworkResponse instance
    Raises:
        PassworkInteractionError
    """

    def __init__(self, url: str, key: str):
        self._url = url
        self._key = key
        self._session = Session()
        self.__token = None

        self._login()
        self.passwords = Passwords(self)

    def __repr__(self) -> str:
        return f'PassworkAPI(url={self._url})'

    @property
    def _headers(self) -> dict[str, str]:
        headers = {'Content-Type': 'application/json'}
        if self.__token:
            headers['Passwork-Auth'] = self.__token
        
        return headers

    def make_request(self,
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

    def _login(self) -> None:
        """
        Login to Passwork API with given key and get auth token string.
        Fetched token writes to self.__token attribute and uses in
        all PasswordAPI requests as 'Passwork-Auth' header value.

        Returns:
            None
        """

        logger.debug('In _login')

        try:
            resp = self.make_request('POST', endpoint=f'/auth/login/{self._key}')
        except PassworkInteractionError as e:
            raise PassworkInteractionError(f'Passwork login failed: {e}')

        self.__token = resp.data['token']

    def _logout(self) -> None:
        """
        Logout from Passwork"""

        logger.debug('In _logout')

        self.make_request('POST', endpoint='/auth/logout')

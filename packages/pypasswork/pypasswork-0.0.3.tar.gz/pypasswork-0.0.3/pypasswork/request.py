"""PassworkAPI base request class"""

import logging
from socket import gaierror
from requests import Request, Session
from requests.exceptions import ConnectionError, ConnectTimeout, JSONDecodeError

from pypasswork.response import PassworkResponse
from pypasswork.exceptions import PassworkInteractionError

logger = logging.getLogger(__name__)


class PassworkRequest:
    def __init__(self, api, verify: bool = True):
        self._api = api
        self._verify = verify

    @property
    def _headers(self) -> dict[str, str]:
        headers = {'Content-Type': 'application/json'}
        if self._api.token:
            headers['Passwork-Auth'] = self._api.token

        return headers

    def __call__(self,
                 method: str,
                 endpoint: str,
                 parameters: dict[str, str] | None = None,
                 timeout: int = 5) -> PassworkResponse:
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

        base_url = f'{self._api.url}/{self._api.root_api}/{endpoint}'

        pw_req = Request(method=method, url=base_url, headers=self._headers, json=parameters).prepare()

        try:
            with Session() as s:
                logger.debug(f'PassworkAPI request: ({pw_req.method}) headers={self._headers}, url={pw_req.url}')
                resp = s.send(request=pw_req, timeout=timeout, verify=self._verify)
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

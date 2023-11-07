import logging

from pypasswork.request import PassworkRequest
from pypasswork.operations.passwords import Passwords
from pypasswork.operations.vaults import Vaults
from pypasswork.operations.folders import Folders


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
        self.url = url
        self.root_api = 'api/v4'
        self._key = key
        self.token = None
        self.req = PassworkRequest(self)
        self.login()

        self.passwords = Passwords(self)
        self.vaults = Vaults(self)
        self.folders = Folders(self)

    def __repr__(self) -> str:
        return f'PassworkAPI(url={self.url})'

    def login(self, print_token: bool = False) -> None:
        """
        Login to Passwork API with given key and get auth token string.
        Fetched token writes to self.__token attribute and uses in
        all PasswordAPI requests as 'Passwork-Auth' header value.

        Parameters:
            print_token: also print retrieved token
        Returns:
            None
        """

        logger.debug('In login')

        resp = self.req('POST', endpoint=f'auth/login/{self._key}')
        token = resp.data['token']
        if print_token:
            print(token)
        self.token = token

    def logout(self) -> None:
        """Logout from Passwork"""

        logger.debug('In logout')

        self.req('POST', endpoint='auth/logout')

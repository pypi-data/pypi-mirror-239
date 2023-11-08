from typing import NoReturn
from requests.models import Response


class ProviderNotFound(Exception):
    """ Raised when provider can not be found by given hostname """

    message: str

    def __init__(self, hostname: str) -> NoReturn:
        self.message = f'Provider not found for hostname {hostname}'
        super().__init__(self.message)


class APIRequestFailed(Exception):
    """ Raised when the API request fails """

    message: str

    def __init__(self, response: Response) -> NoReturn:
        self.message = f'API Request failed with status code {response.status_code}: {response.reason}'
        super().__init__(self.message)

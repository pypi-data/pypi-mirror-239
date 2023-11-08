from typing import Union, Dict, Any
from urllib.parse import urlparse, ParseResult

from videoembed.exceptions import ProviderNotFound
from videoembed.providers.config import PROVIDERS
from videoembed.providers.vimeo import VimeoProvider
from videoembed.providers.youtube import YoutubeProvider


class Embedder(object):

    config: Dict[str, Any]

    def __init__(self, **kwargs):
        self.config = dict(kwargs)

    def __call__(self, url: str):
        return self._get_provider(url, self.config)

    @staticmethod
    def _get_provider(url: str, config: Dict[str, Any]) -> Union[YoutubeProvider, VimeoProvider]:
        parsed_url: ParseResult = urlparse(url)
        for provider, url_patterns in PROVIDERS.items():
            if parsed_url.hostname in url_patterns:
                return provider(url, config)
        raise ProviderNotFound(parsed_url.hostname)

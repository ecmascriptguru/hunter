import json
import urllib.request
from django.conf import settings
from ..models import PROXY_PROVIDER

class ProxyFetcher(object):
    """
    Base class to fetch proxies from proxy providers via API.
    """

    @classmethod
    def get_proxies(cls, url, data={}, method='get'):
        req = urllib.request.Request(url=url)
        with urllib.request.urlopen(req) as response:
            response_test = response.read()
            try:
                json_response = json.loads(response_text)
                return json_response
            except Exception as e:
                raise ValueError('Response is invalid')
                return None
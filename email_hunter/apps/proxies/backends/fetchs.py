import json
import urllib.request
from django.conf import settings
from ..models import Proxy, PROXY_PROVIDER, PROXY_STATE


class ProxyFetcher(object):
    """
    Base class to fetch proxies from proxy providers via API.
    """

    @classmethod
    def fetch_myprivateproxy_proxies(cls):
        access_key = settings.MYPRIVATEPROXY_ACCESS_KEY
        if not access_key:
            raise ImportError("You didn't specified my private proxy api key.")
        
        url = "https://api.myprivateproxy.net/v1/fetchProxies/json/full/showPlanId/{0}".format(access_key)
        items = cls.get_proxies(url)
        created = 0
        updated = 0

        for item in items:
            proxy, _ = Proxy.objects.update_or_create(ip_address=item['proxy_ip'],
                port=item['proxy_port'], provider=PROXY_PROVIDER.MY_PRIVATE_PROXY,
                defaults={'state': PROXY_STATE.active if item['proxy_status'] == 'online' else PROXY_STATE.inactive})
            
            if _:
                created += 1
            else:
                updated += 1
        
        return created, updated

    @classmethod
    def get_proxies(cls, url, data={}, method='get'):
        req = urllib.request.Request(url=url)
        with urllib.request.urlopen(req) as response:
            response_text = response.read()
            try:
                json_response = json.loads(response_text)
                return json_response
            except Exception as e:
                raise ValueError('Response is invalid')
                return None
    
    @classmethod
    def fetch_all(cls, *args, **kwargs):
        created, updated = cls.fetch_myprivateproxy_proxies()
        return created, updated
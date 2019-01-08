# -*- coding: utf-8 -*-
import time

import hashlib
import random
import requests
from selenium.webdriver.common.keys import Keys
from . import TASK_STATES, compute_cur_in_task_meta
from ...apps.targets.models import TargetFile, Target


class GPlusLookup:
    """
    Create session and send POST request to Google services
    to get users json data with email
    """

    base_url = 'https://plus.google.com/people'

    def __init__(self, proxy=None, driver=None):
        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'people-pa.clients6.google.com',
            'Origin': 'https://hangouts.google.com',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
                          '(KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'X-Goog-AuthUser': '0',
            'X-HTTP-Method-Override': 'GET',
        }

        self.timestamp = int(round(time.time() * 1000))

        if proxy:
            self.proxy = {"http"  : "http://{0}".format(proxy.get('address')), 
                            "https" : "https://{0}".format(proxy.get('address'))}
        
        if driver is None:
            raise ValueError('driver is required in Gplus')
        else:
            self.driver = driver

    def open_gplus_people(self):
        self.driver.get(self.base_url)
        time.sleep(random.uniform(0.5, 1.5))

    def find_people(self, email):
        if self.driver.current_url != self.base_url:
            self.open_gplus_people()
        keyword_element = self.driver.find_element_by_css_selector('.Ax4B8')
        keyword_element.send_keys(email)
        time.sleep(random.uniform(1, 2))
        candidates = self.driver.find_elements_by_css_selector('.tWfTvb>.u3WVdc.jBmls .MkjOTb')
        result, info = (False, None)
        if len(candidates) == 2:
            candidate = candidates[0]
            url = candidate.get_attribute('data-url')
            if url and url.startswith('./'):
                result = True
                info = 'https://plus.google.com/' + url[2:]
        
        keyword_element.send_keys(len(email) * Keys.BACKSPACE)
        time.sleep(random.uniform(0.1, 0.5))
        return result, email, info

    def create_authorization_hash(self):
        try:
            cookies = self.driver.get_cookies()
            self.cookies = {}
            for i in cookies:
                self.cookies[i['name']] = i['value']

            hash_auth = hashlib.sha1(str(
                    "%d %s %s" % (self.timestamp, self.cookies['SAPISID'], self.headers['Origin'])
                ).encode('utf-8')).hexdigest()
            authorization = "SAPISIDHASH %d_%s" % (self.timestamp, hash_auth)
            self.headers["Authorization"] = authorization
            return True
        except KeyError as e:
            print(str(e))
            return False

    def _create_data(self, email):
        data = [
            ('id', email),
            ('type', 'EMAIL'),
            ('matchType', 'EXACT'),
            ('requestMask.includeField.paths', 'person.email'),
            ('requestMask.includeField.paths', 'person.gender'),
            ('requestMask.includeField.paths', 'person.in_app_reachability'),
            ('requestMask.includeField.paths', 'person.metadata'),
            ('requestMask.includeField.paths', 'person.name'),
            ('requestMask.includeField.paths', 'person.phone'),
            ('requestMask.includeField.paths', 'person.photo'),
            ('requestMask.includeField.paths', 'person.read_only_profile_info'),
            ('extensionSet.extensionNames', 'HANGOUTS_ADDITIONAL_DATA'),
            ('extensionSet.extensionNames', 'HANGOUTS_OFF_NETWORK_GAIA_LOOKUP'),
            ('extensionSet.extensionNames', 'HANGOUTS_PHONE_DATA'),
            ('coreIdParams.useRealtimeNotificationExpandedAcls', 'true'),
        ]
        return data

    def validate(self, email):
        try:
            time.sleep(random.uniform(1.1, 2.3))
            data = self._create_data(email)
            if self.proxy:
                r = requests.post('https://people-pa.clients6.google.com/v2/people/lookup',
                            headers=self.headers, cookies=self.cookies, data=data, proxies=self.proxy)
            else:
                r = requests.post('https://people-pa.clients6.google.com/v2/people/lookup',
                            headers=self.headers, cookies=self.cookies, data=data)

            if (r.status_code == 200) and (bool(r.json())) and r.text:
                gplus_id = r.json()['matches'][0]['personId'][0]
                email = r.json()['people'][gplus_id]['email'][0]['value']
                return True, email, ("https://plus.google.com/%s" % gplus_id)
            else:
                return False, email, None
        except Exception as e:
            print(str(e))
            return False, email, str(e)

    def get_data(self, candidates, task, meta):
        # if not self.create_authorization_hash():
        #     raise ValueError('Failed to create authorization hash')

        for idx, email in enumerate(candidates):
            meta['pattern'].update(cur=idx, msg='Tyring with {}...'.format(email))
            meta = compute_cur_in_task_meta(meta)
            task.update_state(state=TASK_STATES.in_progress, meta=meta)
            _, email, profile = self.find_people(email)
            
            if _:
                meta['pattern'].update(msg='Found email: {}'.format(email))
                task.update_state(state=TASK_STATES.done, meta=meta)
                return _, email, profile

        return False, None, None
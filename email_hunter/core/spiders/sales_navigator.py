# -*- coding: utf-8 -*-
import time, hashlib, random, requests
from . import TASK_STATES, compute_cur_in_task_meta


class SalesNavigator:
    def __init__(self, *args, **kwargs):
        if not kwargs.get('driver'):
            raise ValueError('driver is required for this.')
        
        self.driver = kwargs.pop('driver')
    
    def validate(self, email):
        time.sleep(random.uniform(0.5, 1.2))
        self.driver.get('https://www.linkedin.com/sales/gmail/profile/viewByEmail/' + email)
        if 'https://www.linkedin.com/sales/gmail/profile/proxy/' + email in self.driver.page_source:
            profile = self.driver.find_element_by_tag_name('a').get_attribute('href')
            return True, email, profile
        elif "Sorry, we couldn't find a matching LinkedIn profile for this email address." in self.driver.page_source:
            return False, email, None
        else:
            print('Unexpected case found(sales navigator)')
            return False, email, None

    def get_data(self, candidates, task, meta):
        for idx, email in enumerate(candidates):
            meta['pattern'].update(cur=idx, msg='Tyring with {}...'.format(email))
            meta = compute_cur_in_task_meta(meta)
            task.update_state(state=TASK_STATES.in_progress, meta=meta)
            _, email, profile = self.validate(email)
            if _:
                meta['pattern'].update(msg='Found email: {}'.format(email))
                task.update_state(state=TASK_STATES.done, meta=meta)
                return True, email, profile
        return False, None, None
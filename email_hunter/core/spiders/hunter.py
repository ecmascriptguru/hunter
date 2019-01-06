"""
Main lib to check email addresses
"""
import requests, json, logging, datetime, time
from os import path
from sys import platform
from django.conf import settings
from ...apps.credentials.models import Credential, CREDENTIAL_STATE
from ...apps.targets.models import Target, TARGET_STATE, TARGET_FILE_STATE
from ...apps.jobs.models import Job, JOB_STATE
from ...apps.leads.models import Lead, LEAD_FOUND_ENGING
from .browser import Browser
from .gplus import GPlusLookup
from .sales_navigator import SalesNavigator
from . import TASK_STATES


class Hunter:
    """
    Hunter module
    """
    default_meta = {
            'current': 0, 'total': 1,
            'prepare': { 'cur': 0, 'total': 1, 'msg': 'Waiting for browser to be initialized...' },
            'candidates': { 'cur': 0, 'total': 1, 'msg': 'Waiting for browser to be prepared...' },
            'step': { 'cur': 0, 'total': 2, 'msg': '' },
            'pattern': { 'cur': 0, 'total': 26, 'msg': ''},
        }

    def __init__(self, task, count, *args, **kwargs):
        task.update_state(state=TASK_STATES.pending, meta=self.default_meta)
        self.task = task
        self.default_meta['candidates'].update({ 'total': count })
        if Credential.is_available():
            cred = Credential.actives().first()
            self.browser = Browser(*args, **kwargs, pk=cred.pk)
        else:
            self.task.update_state(state=TASK_STATES.failed, meta=self.default_meta)
            self.stop(job_state=JOB_STATE.got_error)
            raise ValueError('Credential is not available.')
        
        if task and task.request.id:
            self.set_job(task.request.id)
    
    def take_screenshot(self):
        dir = path.join(settings.BASE_DIR, 'static/issues')
        return self.browser.save_screenshot(path.join(dir, str(datetime.datetime.now()) + '.png'))

    def update_task_state(self, state=TASK_STATES.in_progress):
        if self.task:
            self.task.update_state(state=state, meta=self.default_meta)
    
    def set_job(self, job_uuid):
        self.job = Job.objects.get(internal_uuid=job_uuid)
        self.set_job_state(state=JOB_STATE.in_progress)
        self.task.update_state(state=TASK_STATES.in_progress, meta=self.default_meta)

        if not self.browser.is_prepared:
            self.update_task_state(state=TASK_STATES.failed)
            self.take_screenshot()
            raise Exception('Browser is not ready to get started.')
        else:
            self.default_meta['prepare'].update({
                'cur': 1,
                'msg': 'Browser is prepared to validate email addresses.'
            })
            self.update_task_state()

        self.gplus = GPlusLookup(proxy=self.browser.proxy, driver=self.browser)
        self.salesNavigator = SalesNavigator(driver=self.browser)

    def set_job_state(self, state=JOB_STATE.completed):
        if self.job:
            if self.job.state != state:
                self.job.state = state
                self.job.save()
            
            if self.job.file and state in [JOB_STATE.completed, JOB_STATE.got_error]:
                file = self.job.file
                if not file.has_pending_or_in_progress_jobs:
                    file.state = TARGET_FILE_STATE.done
                    file.save()
        else:
            print("This task has not been executed by any file.")

    def validate(self, target_id, index=0):
        target = Target.objects.get(pk=target_id)
        target.state = TARGET_STATE.in_progress
        target.save()
        self.default_meta['candidates'].update({ 'cur': index + 1, 'msg': 'Analyzing {}'.format(target.full_name) })

        self.first_name = target.first_name
        self.last_name = target.last_name
        self.domain = target.domain

        candidates = self.generate_emails(self.domain, self.first_name, self.last_name)
        found_engine = LEAD_FOUND_ENGING.gplus
        lead = None
        self.default_meta['step'].update({ 'cur': 1, 'msg': 'Validating {} with Google+ API'.format(target.full_name) })
        _, email, info = self.gplus.get_data(candidates, self.task, self.default_meta)

        if not _:
            found_engine = LEAD_FOUND_ENGING.linkedin
            self.default_meta['step'].update({ 'cur': 2, 'msg': 'Validating {} with LinkedIn API'.format(target.full_name) })
            _, email, info = self.salesNavigator.get_data(candidates, self.task, self.default_meta)

        target = Target.objects.get(pk=target_id)
        if _:
            target.state = TARGET_STATE.validated
            # Should something to save lead
            lead = Lead.objects.create(target=target, found_by=target.created_by,
                    engine=found_engine, profile=info, email=email)
        else:
            target.state = TARGET_STATE.failed
        
        target.save()
        return _, lead

    def stop(self, job_state=JOB_STATE.completed):
        self.set_job_state(state=job_state)
        self.browser.quit(state=CREDENTIAL_STATE.active)
        return self.default_meta
    
    def generate_emails(self, domain, first_name, last_name):
        """
        docstring for generate_emails
        """
        email_list = []
        fn_initial = first_name[:1]
        ln_initial = last_name[:1]

        email_list.append(['{}@{}'.format(first_name, domain)])
        email_list[0].extend(
            [
                '{}@{}'.format(last_name, domain),
                '{}{}@{}'.format(first_name, last_name, domain),
                '{}.{}@{}'.format(first_name, last_name, domain),
                '{}{}@{}'.format(fn_initial, last_name, domain),
                '{}.{}@{}'.format(fn_initial, last_name, domain),
                '{}{}@{}'.format(first_name, ln_initial, domain),
                '{}.{}@{}'.format(first_name, ln_initial, domain),
                '{}{}@{}'.format(last_name, first_name, domain),
                '{}.{}@{}'.format(last_name, first_name, domain),
                '{}{}@{}'.format(last_name, fn_initial, domain),
                '{}.{}@{}'.format(last_name, fn_initial, domain),
                '{}{}@{}'.format(ln_initial, first_name, domain),
                '{}.{}@{}'.format(ln_initial, first_name, domain),
                '{}{}@{}'.format(ln_initial, fn_initial, domain),
                '{}-{}@{}'.format(first_name, last_name, domain),
                '{}-{}@{}'.format(fn_initial, last_name, domain),
                '{}-{}@{}'.format(first_name, ln_initial, domain),
                '{}-{}@{}'.format(last_name, first_name, domain),
                '{}-{}@{}'.format(last_name, fn_initial, domain),
                '{}_{}@{}'.format(first_name, last_name, domain),
                '{}_{}@{}'.format(fn_initial, last_name, domain),
                '{}_{}@{}'.format(first_name, ln_initial, domain),
                '{}_{}@{}'.format(last_name, first_name, domain),
                '{}_{}@{}'.format(last_name, fn_initial, domain),
                '{}_{}@{}'.format(ln_initial, first_name, domain),
            ])
        email_list.append(
            [
                '{}{}@gmail.com'.format(first_name, last_name),
                '{}.{}@gmail.com'.format(first_name, last_name),
                '{}{}@gmail.com'.format(fn_initial, last_name),
                '{}.{}@gmail.com'.format(fn_initial, last_name),
                '{}{}@gmail.com'.format(first_name, ln_initial),
                '{}.{}@gmail.com'.format(first_name, ln_initial),
                '{}{}@gmail.com'.format(last_name, first_name),
                '{}.{}@gmail.com'.format(last_name, first_name),
                '{}{}@gmail.com'.format(ln_initial, first_name),
                '{}.{}@gmail.com'.format(ln_initial, first_name),
                '{}-{}@gmail.com'.format(first_name, last_name),
                '{}-{}@gmail.com'.format(fn_initial, last_name),
                '{}-{}@gmail.com'.format(first_name, ln_initial),
                '{}-{}@gmail.com'.format(last_name, first_name),
                '{}-{}@gmail.com'.format(last_name, fn_initial),
                '{}_{}@gmail.com'.format(first_name, last_name),
                '{}_{}@gmail.com'.format(fn_initial, last_name),
                '{}_{}@gmail.com'.format(first_name, ln_initial),
                '{}_{}@gmail.com'.format(last_name, first_name),
            ])

        # return {
        #     'domain': domain,
        #     'first_name': first_name,
        #     'last_name': last_name,
        #     'emails': {
        #         'custom_domain': email_list[0],
        #         'gmail.com': email_list[1]
        #     }
        # }
        return email_list[0]
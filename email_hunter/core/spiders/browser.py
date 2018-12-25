"""
User Defined Selenium Browser
"""

import json, datetime, csv, logging, sys, time
import os, requests, tldextract
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from sys import platform
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from ...apps.credentials.models import Credential, CREDENTIAL_STATE


class Browser(webdriver.Chrome):
    """Main Browser to be used in validation.
    -  credential: required in constructor
    """
    credential_pk = None
    email = None
    password = None
    proxy = None
    recovery_email = None
    recovery_phone = None
    _is_prepared = False

    chromedriver_path = settings.CHROME_DRIVER_PATH

    recovery_option_link_class_name = 'C5uAFc'
    recovery_phone_number_option_text = 'Confirm your recovery phone number'
    recovery_email_option_text = 'Confirm your recovery email'
    recovery_email_error_text = 'The email you entered is incorrect. Try again.'

    _google_login_check_count = 0

    _element_find_timer = 0

    def __init__(self, *args, **kwargs):
        if not kwargs.get('pk', None):
            credential = Credential.get_hold()
        else:
            credential = Credential.objects.get(pk=kwargs.pop('pk'))

        if credential is None:
            raise ImproperlyConfigured('credential is required.')

        self.set_credential(credential)
        super(Browser, self).__init__(self.chromedriver_path, options=self.get_options(),
                desired_capabilities=self.get_desired_capabilities())
    
    def get_options(self):
        if platform != 'win32' and not settings.DEBUG:
            self.display = Display(visible=0, size=(1200, 900))
            self.display.start()

        if not os.path.exists(self.chromedriver_path):
            raise ImproperlyConfigured('Chrome driver file doesn\' exist.')

        options = webdriver.ChromeOptions()
        options.add_argument("--window-size=1200,900")
        options.add_argument('--dns-prefetch-disable')
        options.add_argument('--js-flags="--max_old_space_size=4096"')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')

        # Should be enabled
        if not settings.DEBUG:
            options.add_argument("--headless")
            
            prefs = {"profile.managed_default_content_settings.images":2}
            options.add_experimental_option("prefs",prefs)

        return options
    
    def get_desired_capabilities(self):
        capabilities = dict(DesiredCapabilities.CHROME)
        capabilities['proxy'] = {'proxyType': 'MANUAL',
                                'httpProxy': self.proxy.get('address'),
                                'ftpProxy': self.proxy.get('address'),
                                'sslProxy': self.proxy.get('address'),
                                'noProxy': '',
                                'class': "org.openqa.selenium.Proxy",
                                'autodetect': False}
        return capabilities

    def set_credential(self, credential):
        credential.state = CREDENTIAL_STATE.using
        credential.save()

        self.email = credential.email
        self.password = credential.password
        self.proxy = credential.proxy.to_json
        self.credential_pk = credential.pk
        self.recovery_email = credential.recovery_email
        self.recovery_phone = credential.recovery_phone

    @property
    def credential(self):
        return Credential.objects.get(pk=self.credential_pk)
    
    def rollback_credential_state(self, state=CREDENTIAL_STATE.hold):
        try:
            credential = self.credential
            if credential.state in [CREDENTIAL_STATE.processing, CREDENTIAL_STATE.using]:
                credential.state = state
                credential.save()
        except Credential.DoesNotExists as e:
            raise Credential.DoesNotExists('Credential Not Found.')

    def quit(self, *args, **kwargs):
        if platform != 'win32' and not settings.DEBUG:
            self.display.stop()

        self.rollback_credential_state(**kwargs)
        super(Browser, self).quit()

    def is_logged_into_linkedIn(self):
        if 'Adding a phone number adds security' in self.page_source:
            self._element_find_timer = 0
            el = self.find_element_by_class_name('secondary-action')
            if el is None:
                return False
            el.click()
            time.sleep(2)

        while(self._linkedin_login_check_count < 3):
            if self.current_url == "https://www.linkedin.com/feed/" or self.current_url == 'https://www.linkedin.com/hp/':
                print('LinkedIn is ready')
                return True
            elif False:
                # Logic to check google reCaptcha should be implemented here.
                pass
            else:
                print("Keeping wait for browser to log into linkedIn...({0})".format(self._linkedin_login_check_count))
                self._linkedin_login_check_count += 1
                time.sleep(2)

        print('Something went wrong with LinkedIn')
        return False

    def login_linkedin(self):
        """
        login to LinkedIn
        """
        if not self.email or not self.password:
            raise NotImplementedError('Not implemented.')

        print("Login to LinkedIn...")
        self.get('https://www.linkedin.com/')
        time.sleep(1)

        try:
            self._element_find_timer = 0
            el = self.find_element_by_css_selector('#login-email')
            if el is None:
                return False
            el.send_keys(self.email)

            self._element_find_timer = 0
            el = self.find_element_by_css_selector('#login-password')
            if el is None:
                return False
            el.send_keys(self.password)
            
            self._element_find_timer = 0
            self.find_element_by_css_selector('#login-submit').click()
            if el is None:
                return False
            time.sleep(2)

            self._linkedin_login_check_count = 0
        except Exception as e:
            print(str(e))
            return False
        return self.is_logged_into_linkedIn()

    def is_logged_into_gmail(self):
        '''
        check if we have successful login
        :return: function don't return anything
        '''

        while(self._google_login_check_count < 3):
            if self.current_url.startswith('https://mail.google.com/'):
                print('Gmail is ready')
                return True
            else:
                print("Keeping wait for browser to log into google...({0})".format(self._google_login_check_count))
                self._google_login_check_count += 1
                time.sleep(2)

        print('Something went wrong with gmail')
        return False

    def should_verify_google(self):
        return (self.recovery_phone_number_option_text in self.page_source or
                self.recovery_email_option_text in self.page_source)

    def verify_google_account_with_recovery_info(self):
        found = False
        try:
            els = self.find_elements_by_css_selector("." + self.recovery_option_link_class_name)
        
            for el in els:
                if self.recovery_email_option_text in el.text:
                    el.click()
                    found = 'email'
                    break
                elif self.recovery_phone_number_option_text in el.text:
                    el.click()
                    found='phone_number'
                    break
            
            if not found:
                # Should do something in this case...
                return False

            time.sleep(10)
            
            print(found)
            if found == 'email':
                email_box = self.find_element_by_id('identifierId')
                print(email_box)
                email_box.send_keys(self.recovery_email)
            elif found == 'phone_number':
                phone_number_box = self.find_element_by_id('phoneNumberId')
                print(phone_number_box)
                phone_number_box.send_keys(self.recovery_phone)
            else:
                print('something went wrong')

            action_buttons = self.find_elements_by_css_selector('span.RveJvd.snByac')
            next_button = action_buttons[0]
            try_another_button = action_buttons[1]
            next_button.click()
            time.sleep(3)

            if self.email in self.page_source and self.recovery_email in self.page_source:
                done_button = self.find_elements_by_css_selector('span.RveJvd.snByac')[1]
                done_button.click()
                return True
            else:
                print('Unknown case found.')
                return False
        except Exception as e:
            print(str(e))
            return False
        
        return True
        
    def login_gmail(self):
        """
        login to GMail
        """
        if not self.email or not self.password:
            raise NotImplementedError('Not implemented.')

        print("Logging into Gmail")
        self.get('https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Fmail.google.com')
        time.sleep(1)
        
        try:
            self._element_find_timer = 0
            el = self.find_element_by_css_selector('#identifierId')
            if el is None:
                return False
            el.send_keys(self.email)

            self._element_find_timer = 0
            el = self.find_element_by_id('identifierNext')
            if el is None:
                return False
            el.click()
            time.sleep(10)

            self._element_find_timer = 0
            el = self.find_element_by_name('password')
            if el is None:
                return False
            el.send_keys(self.password)

            self._element_find_timer = 0
            el = self.find_element_by_id('passwordNext')
            if el is None:
                return False
            el.click()
            time.sleep(10)

            print("HERE")
            if self.should_verify_google():
                self.verify_google_account_with_recovery_info()

            self._google_login_check_count = 0
        except Exception as e:
            print(str(e))
        finally:
            return self.is_logged_into_gmail()

    @property
    def is_prepared(self):
        if not self._is_prepared:
            self._is_prepared = (self.login_linkedin() and self.login_gmail())
        
        if self._is_prepared:
            self.rollback_credential_state(state=CREDENTIAL_STATE.active)
        else:
            self.rollback_credential_state()
        
        return self._is_prepared

    def recovery_account(self):
        print("Recovering account {}...".format(self.email))
        return self.is_prepared
    
    # Override of default methods of super class
    # to let it try to find elements 10 times
    def find_element_by_css_selector(self, selector):
        try:
            return super(Browser, self).find_element_by_css_selector(selector)
        except Exception as e:
            print(str(e), self._element_find_timer)
            time.sleep(2)
            self._element_find_timer += 1
            if self._element_find_timer < 10:
                return self.find_element_by_css_selector(selector)
            else:
                return None
    def find_elements_by_css_selector(self, selector):
        try:
            return super(Browser, self).find_elements_by_css_selector(selector)
        except Exception as e:
            print(str(e), self._element_find_timer)
            time.sleep(2)
            self._element_find_timer += 1
            if self._element_find_timer < 10:
                return self.find_elements_by_css_selector(selector)
            else:
                return []

    def find_element_by_id(self, selector):
        try:
            return super(Browser, self).find_element_by_id(selector)
        except Exception as e:
            print(str(e), self._element_find_timer)
            time.sleep(2)
            self._element_find_timer += 1
            if self._element_find_timer < 10:
                return self.find_element_by_id(selector)
            else:
                return None

    def find_element_by_name(self, selector):
        try:
            return super(Browser, self).find_element_by_name(selector)
        except Exception as e:
            print(str(e), self._element_find_timer)
            time.sleep(2)
            self._element_find_timer += 1
            if self._element_find_timer < 10:
                return self.find_element_by_name(selector)
            else:
                return None

    def find_element_by_class_name(self, selector):
        try:
            return super(Browser, self).find_element_by_class_name(selector)
        except Exception as e:
            print(str(e), self._element_find_timer)
            time.sleep(2)
            self._element_find_timer += 1
            if self._element_find_timer < 10:
                return self.find_element_by_class_name(selector)
            else:
                return None

    def find_elements_by_class_name(self, selector):
        try:
            return super(Browser, self).find_elements_by_class_name(selector)
        except Exception as e:
            print(str(e), self._element_find_timer)
            time.sleep(2)
            self._element_find_timer += 1
            if self._element_find_timer < 10:
                return self.find_elements_by_class_name(selector)
            else:
                return []
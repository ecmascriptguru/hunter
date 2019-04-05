import time, random
from .browser import Browser, Chrome
from email_hunter.apps.google_accounts.models import GoogleAccount


class BacklinkHunter(Browser):
    credential_class = GoogleAccount
    search_console_base_url = 'https://search.google.com/search-console/links'
    gplus_success_url = 'https://mail.google.com/'

    def __init__(self, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            pk = self.credential_class.objects.first().id

        print(pk)
        super(BacklinkHunter, self).__init__(*args, pk=pk, **kwargs)
        # self.login_gmail()
    
    def open_search_console(self):
        self.get(self.search_console_base_url)
    
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
                return self.unlock_google_account()
            el.send_keys(self.email)

            self._element_find_timer = 0
            el = self.find_element_by_id('identifierNext')
            if el is None:
                return self.unlock_google_account()
            el.click()
            time.sleep(random.uniform(3.5, 5))

            self._element_find_timer = 0
            el = self.find_element_by_name('password')
            if el is None:
                return self.unlock_google_account()
            el.send_keys(self.password)

            self._element_find_timer = 0
            el = self.find_element_by_id('passwordNext')
            if el is None:
                el = self.find_element_by_css_selector('#signIn')
                if el is None:
                    return False
            el.click()
            time.sleep(random.uniform(3.5, 5))

            if self.should_verify_google():
                self.verify_google_account_with_recovery_info()

            self._google_login_check_count = 0
        except Exception as e:
            print(str(e))
            self.take_screenshot()
        finally:
            return self.is_logged_into_gmail()

    def get_properties(self):
        link = self.find_element_by_css_selector("div.U26fgb.mUbCce.fKz7Od.wfDTAc")
        link.click()
        time.sleep(1)
        dropdowns = self.find_elements_by_css_selector(".s3ARzb.eejsDc div.iPVm1b div.utePyc")
        properties = list()
        for item in dropdowns:
            properties.append(item.text)
        
        return properties
    
    def get_backlinks(self, website):
        # Getting url for specific website
        link = "%s?resource_id=%s" % (self.search_console_base_url, website)
        self.get(link)

        # click export button
        export_external_button = self.find_element_by_css_selector("span.NlWrkb.snByac div.gIhoZ")
        export_external_button.click()
        time.sleep(random.uniform(0.2, 0.8))

        # Choose a dropdown menuitem to get latest links
        latest_links_dropdown = self.find_elements_by_css_selector("content. div.uyYuVb.oJeWuf")[1]
        latest_links_dropdown.click()
        time.sleep(random.uniform(0.2, 0.8))

        # Choose CSV Format to download
        csv_link = self.find_element_by_css_selector("div.g3VIld.N7pFaf.Up8vH.hFEqNb.J9Nfi.iWO5td content.z80M1")
        csv_link.click()
    
    def get_report(self):
        properties = self.get_properties()
        for website in properties:
            self.get_backlinks(website)

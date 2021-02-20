import warnings
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from form import myconstants
from requests_html import HTMLSession
import requests
from time import sleep
import random
from form import form_extractor
import custom_website_functions
warnings.filterwarnings("ignore")


class CustomSweepstakes:
    def __init__(self, session, urls_list_file):
        self.session = session
        self.urls = []
        self.new_urls = []
        self.expired_urls = []
        self.urls_list_file = urls_list_file
        self.urls = self.get_urls()

    def get_urls(self):
        url_file = open(self.urls_list_file, 'r')
        urls = [line for line in url_file.readlines() if line.strip()]
        url_file.close()
        return urls

    def submit_form(self, url, name, email):
        forms = form_extractor.get_all_forms(self.session, url)
        # get the first form with a post method
        form_details = form_extractor.get_all_post_forms(forms)[0]

        data = custom_website_functions.get_custom_form(form_details=form_details,
                                                        name=name,
                                                        email=email)

        submit_url = urljoin(myconstants.BASE_URL, form_details["action"])
        res = self.session.post(submit_url, data=data)
        return res

    def submit_entry(self, email, entry_num, entry_url):
        result = self.submit_form(entry_url, myconstants.NAME, email)
        website_return_value = result.request.path_url
        # custom return type -> this can be different depending on the website
        if custom_website_functions.check_success(website_return_value=website_return_value):
            # logging.info(f'submitted entry number {entry_num} for email {email}.')
            # logging.info(f'{result.status_code} : {result.reason}')
            return True

        # logging.error(f'Entry number {entry_num} not submitted for email {email}')
        print(f'Entry number {entry_num} not submitted for email {email}')
        return False

    def submit_entries(self, entry_url, entry_limit=1, sleep_waittime=5):
        # logging.info(f'url: {entry_url} is before deadline, submitting entries')
        for email in myconstants.EMAILS:
            for entry_num in range(1, entry_limit + 1):
                result = self.submit_entry(email, entry_num, entry_url)
                if not result:
                    break
                sleep(sleep_waittime)
        # add some wait times to reduce spam
        sleep(random.randint(1, 5))

    def run_sweepstakes(self):
        new_urls = []
        expired_urls = []
        for url_count, url in enumerate(set(self.urls)):
            url = url.strip()
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            results = soup.findAll('p') # get parsed webpage

            if custom_website_functions.is_before_deadline(results):
                new_urls.append(url)
                self.submit_entries(url, custom_website_functions.get_entry_limit(results), 5)
                print(f"Submitted {url}")
            else:
                expired_urls.append(url)
                print(f"Expired {url}")
            urls_left_count = len(set(self.urls)) - url_count - 1
            print(f"{urls_left_count} URLs left!")

        self.new_urls = new_urls
        self.expired_urls = expired_urls
        self.session.close()

    def overwrite_url_file(self):
        with open(self.urls_list_file, 'w') as url_file_overwrite:
            for item in self.new_urls:
                url_file_overwrite.write("%s\n" % item)

    def print_expired_urls(self):
        if self.expired_urls:
            print("Expired URLs:")
            for url in self.expired_urls:
                print(url)


if __name__ == '__main__':
    # logging.basicConfig(filename=f"../logs/logfile_{datetime.today()}.log", level=logging.INFO)
    customSweepstakes = CustomSweepstakes(HTMLSession(), myconstants.LIST_URLS_FILE)
    customSweepstakes.run_sweepstakes()
    customSweepstakes.print_expired_urls()
    customSweepstakes.overwrite_url_file()

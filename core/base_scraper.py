import requests
from utils.utils import get_settings, mkdirs, get_cookies

from abc import ABC, abstractmethod

class BaseScraper(ABC):
    requests_count = 0
    cookies = None
    headers = ''
    cursor = ''
    username = 'abc'
    
    tweets = []

    def __init__(self, limit):
        self.settings = get_settings()
        mkdirs(self.settings.get('DATA_DIR'))
        self.limit = limit

    def request(self, url):
        r = requests.get(url, headers=self.headers, cookies=self.extract_cookies(self.cookies))
        self.requests_count += 1
        return r
    
    def extract_cookies(self, selenium_cookies):
        cookies = {}
        for cookie in selenium_cookies:
            cookies[cookie['name']] = cookie['value']
        return cookies
    
    def update_cookies(self, username=False):
        cookies, headers, userid, url_profile_token = get_cookies(username)
        if cookies:
            self.cookies = cookies
            self.headers = headers
            self.userid = userid
            self.url_profile_token = url_profile_token
    
    @abstractmethod
    def start_request(self, cursor=None):
        if self.requests_count%self.settings.get('REFRESH_RATE') == 0:
            self.update_cookies(self.username)
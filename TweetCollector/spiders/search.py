import re, json, logging
from urllib.parse import quote

from scrapy.exceptions import CloseSpider
from scrapy import http
from scrapy.spiders import CrawlSpider
from scrapy.shell import inspect_response
from scrapy.core.downloader.middleware import DownloaderMiddlewareManager
from scrapy_selenium import SeleniumRequest, SeleniumMiddleware

from TweetCollector.items import Tweet, User
from TweetCollector.utils import get_cookies

logger = logging.getLogger(__name__)

class SearchSpider(CrawlSpider):
    name = 'search'
    allowed_domains = ['twitter.com']

    def __init__(self, query='', **kwargs):
        if kwargs.get('username', None):
            query += f" from:{kwargs.get('username')}"
        if kwargs.get('year', None):
            query += f" until:{kwargs.get('year')}"
        if kwargs.get('since', None):
            query += f" since:{kwargs.get('since')}"
        if kwargs.get('until', None):
            query += f" until:{kwargs.get('until')}"

        self.url = (
            f'https://twitter.com/i/api/2/search/adaptive.json?'
            f'include_profile_interstitial_type=1'
            f'&include_blocking=1'
            f'&include_blocked_by=1'
            f'&include_followed_by=1'
            f'&include_want_retweets=1'
            f'&include_mute_edge=1'
            f'&include_can_dm=1'
            f'&include_can_media_tag=1'
            f'&skip_status=1'
            f'&cards_platform=Web-12'
            f'&include_cards=1'
            f'&include_ext_alt_text=true'
            f'&include_quote_count=true'
            f'&include_reply_count=1'
            f'&tweet_mode=extended'
            f'&include_entities=true'
            f'&include_user_entities=true'
            f'&include_ext_media_color=true'
            f'&include_ext_media_availability=true'
            f'&send_error_codes=true'
            f'&simple_quoted_tweet=true'
            f'&query_source=typed_query'
            f'&pc=1'
            f'&spelling_corrections=1'
            f'&ext=mediaStats%2ChighlightedLabel'
            f'&count=20'
            f'&tweet_search_mode=live'
        )
        self.url = self.url + '&q={query}'
        self.query = query
        
        self.num_search_issued = 0
        # regex for finding next cursor
        self.cursor_re = re.compile('"(scroll:[^"]*)"')

        self.limit = int(kwargs.get('limit', 0))
        self.at_limit = False

    def start_requests(self):
        yield SeleniumRequest(url="https://twitter.com/explore", callback=self.parse_home_page)


    def parse_home_page(self, response):
        self.update_cookies(response)
        for r in self.start_query_request():
            yield r

    def update_cookies(self, response):
        driver = response.meta['driver']
        cookies, headers = get_cookies(driver)
        if cookies:
            self.cookies = cookies
            self.headers = headers

    def start_query_request(self, cursor=None):
        if cursor:
            url = self.url + '&cursor={cursor}'
            url = url.format(query=quote(self.query), cursor=quote(cursor))
        else:
            url = self.url.format(query=quote(self.query))
        request = http.Request(url, callback=self.parse_result_page, cookies=self.cookies, headers=self.headers)
        yield request

        self.num_search_issued += 1
        if self.num_search_issued % 100 == 0:
            # get new SeleniumMiddleware            
            for m in self.crawler.engine.downloader.middleware.middlewares:
                if isinstance(m, SeleniumMiddleware):
                    m.spider_closed()
            self.crawler.engine.downloader.middleware = DownloaderMiddlewareManager.from_crawler(self.crawler)
            # update cookies
            yield SeleniumRequest(url="https://twitter.com/explore", callback=self.update_cookies, dont_filter=True)


    def parse_result_page(self, response):
        if self.at_limit:
            raise CloseSpider('Limit Reached')
        data = json.loads(response.text)
        for item in self.parse_tweet_item(data['globalObjects']['tweets']):
            yield item
        for item in self.parse_user_item(data['globalObjects']['users']):
            yield item

        # get next page
        cursor = self.cursor_re.search(response.text).group(1)
        for r in self.start_query_request(cursor=cursor):
            yield r


    def parse_tweet_item(self, items):
        for k,v in items.items():
            tweet = Tweet()
            tweet['id_'] = k
            tweet['tweet'] = v
            yield tweet


    def parse_user_item(self, items):
        for k,v in items.items():
            user = User()
            user['id_'] = k
            user['user'] = v
            yield user

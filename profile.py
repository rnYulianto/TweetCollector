import json
import requests
import argparse
from datetime import datetime
from urllib.parse import quote, unquote

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from utils import get_cookies

class Profile():
    requests_count = 0
    user_tweets_url = "https://twitter.com/i/api/graphql/{user_tweets_url_token}/UserTweets?variables="
    url_params = {
        "userId":"",
        "count":40,
        "includePromotedContent":True,
        "withQuickPromoteEligibilityTweetFields":True,
        "withSuperFollowsUserFields":True,
        "withDownvotePerspective":False,
        "withReactionsMetadata":False,
        "withReactionsPerspective":False,
        "withSuperFollowsTweetFields":True,
        "withVoice":True,
        "withV2Timeline":False,"__fs_dont_mention_me_view_api_enabled":False,"__fs_interactive_text_enabled":False,"__fs_responsive_web_uc_gql_enabled":False}

    cookies = ''
    headers = ''
    userid = ''
    url_profile_token = {}

    tweets = []

    def __init__(self, username, limit):
        self.username = username
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

    def update_cookies(self, username):
        self.cookies, self.headers, self.userid, self.url_profile_token = get_cookies(username)
        self.url_params['userId'] = self.userid

    def get_url(self, url, params):
        params_q = quote(json.dumps(params))
        return url + params_q

    def get_cursor_id(self, entries):
        cursor_bottom = [tweet for tweet in entries['entries'] if 'cursor-bottom' in tweet['entryId']]
        if len(cursor_bottom) < 1:
            return ''
        return cursor_bottom[0]['content']['value']

    def start_request(self, cursor=None):
        if self.requests_count%100 == 0:
            self.update_cookies(self.username)

        if cursor:
            self.url_params['cursor'] = cursor
            cur_url = self.get_url(
                self.user_tweets_url.format(user_tweets_url_token=self.url_profile_token['userTweets']),
                self.url_params
            )
        else:
            cur_url = self.get_url(
                self.user_tweets_url.format(user_tweets_url_token=self.url_profile_token['userTweets']),
                self.url_params
            )

        r = self.request(cur_url)

        res_json = r.json()
        res_data = res_json['data']['user']['result']['timeline']['timeline']['instructions']
        tweet_entries = [entries for entries in res_data if entries['type'] == 'TimelineAddEntries'][0]
        cur_tweet = [tweet for tweet in tweet_entries['entries'] if 'tweet' in tweet['entryId']]
        if len(cur_tweet) > 0 and (self.limit == 0 or len(self.tweets)<self.limit):
            cursor = self.get_cursor_id(tweet_entries)
            cur_tweet = [tweet['content']['itemContent']['tweet_results']['result']['legacy'] for tweet in cur_tweet]
            self.tweets += cur_tweet
            
            self.start_request(cursor)
        else:
            date_now = datetime.now().strftime("%H-%M-%S %d-%m-%Y")
            with open(f'{self.username}-tweets_{date_now}.json', 'w') as outfile:
                json.dump(self.tweets, outfile)

parser = argparse.ArgumentParser(description='Script to get tweet from certain user.')
parser.add_argument("-u", "--username")
parser.add_argument("-l", "--limit", default=0, type=int)
args = parser.parse_args()

if args.username == '':
    print('You need to specify the username')
    exit()
else:
    p = Profile(args.username, args.limit)
    p.start_request()
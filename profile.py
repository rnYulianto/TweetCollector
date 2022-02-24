import json
import argparse
from datetime import datetime
from urllib.parse import quote
from core.base_scraper import BaseScraper

class Profile(BaseScraper):
    base_url = "https://twitter.com/i/api/graphql/{user_tweets_url_token}/UserTweets?variables="
    # base_url = "https://twitter.com/i/api/graphql/{user_tweets_url_token}/UserTweetsAndReplies?variables="
    url_params = {
        # "withCommunity": True,
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
    
    def __init__(self, username, limit):
        super().__init__(limit)
        self.username = username

    def update_cookies(self, username):
        super().update_cookies(username)
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
        super().start_request(cursor)

        if cursor:
            self.url_params['cursor'] = cursor
            cur_url = self.get_url(
                self.base_url.format(user_tweets_url_token=self.url_profile_token['userTweets']),
                self.url_params
            )
        else:
            cur_url = self.get_url(
                self.base_url.format(user_tweets_url_token=self.url_profile_token['userTweets']),
                self.url_params
            )

        r = self.request(cur_url)

        res_json = r.json()
        res_data = res_json['data']['user']['result']['timeline']['timeline']['instructions']
        tweet_entries = [entries for entries in res_data if entries['type'] == 'TimelineAddEntries'][0]

        cur_cursor = self.get_cursor_id(tweet_entries)
        cur_tweet = [tweet for tweet in tweet_entries['entries'] if 'tweet' in tweet['entryId']]
        cur_tweet = [tweet['content']['itemContent']['tweet_results']['result']['legacy'] for tweet in cur_tweet]
        self.tweets += cur_tweet

        print(f'Tweet in memory = {len(self.tweets)}')
        print(f'Limit = {self.limit}')
        print(f'cursor = {cursor}, next cursor = {cur_cursor}')
        print('---------------------------------------------------------')

        if (cur_cursor != cursor  and self.limit == 0) or len(self.tweets)<self.limit:
            self.start_request(cur_cursor)
        else:
            date_now = datetime.now().strftime("%H-%M-%S %d-%m-%Y")
            with open(self.settings.get('DATA_DIR') / f'{self.username}-tweets_{date_now}.json', 'w') as outfile:
                json.dump(self.tweets, outfile)

parser = argparse.ArgumentParser(description='Script to get tweet from certain user.')
parser.add_argument("-u", "--username")
parser.add_argument("-l", "--limit", default=0, type=int)
args = parser.parse_args()

p = Profile(args.username, args.limit)
p.start_request()
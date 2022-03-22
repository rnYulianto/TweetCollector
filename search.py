from ast import arg
from cmath import sin
import re
import json
import argparse
from datetime import datetime
from urllib.parse import quote

from numpy import source
from core.base_scraper import BaseScraper

class Search(BaseScraper):
    cursor_re = re.compile('"(scroll:[^"]*)"')
    users = []
    base_url = (
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
    ) + '&q={query}'
    

    def __init__(self, query, username, limit, year, since, until):
        super().__init__(limit)
        self.query = query
        self.judul = query # menambah variabel judul
        if username:
            self.query += f" from:{username}"
            self.judul += f" from_{username}"
        if year:
            self.query += f" until:{year}"
            self.judul += f" year_{year}"
        if since:
            self.query += f" since:{since}" 
            self.judul += f" since_{since}"
        if until:
            self.query += f" until:{until}"
            self.judul += f" until_{until}"

    def get_url(self, url, query, cursor=None):
        if cursor:
            return url.format(query=quote(query), cursor=quote(cursor))
        else:
            return url.format(query=quote(query))

    def start_request(self, cursor=None):
        super().start_request(cursor)

        if cursor:
            self.base_url += '&cursor={cursor}'
            cur_url = self.get_url(
                self.base_url,
                self.query,
                cursor
            )
        else:
            cur_url = self.get_url(
                self.base_url,
                self.query
            )
        
        r = self.request(cur_url)
        print(r.text)
        try:
            cur_cursor = self.cursor_re.search(r.text).group(1)
            res_json = r.json()
            cur_tweets = res_json['globalObjects']['tweets']
            cur_users = res_json['globalObjects']['users']
            for t in cur_tweets:
                self.tweets.append(cur_tweets[t])
            for u in cur_users:
                self.users.append(cur_users[u])
        except:
            cur_cursor = cursor

        print(f'Tweet in memory = {len(self.tweets)}')
        print(f'Limit = {self.limit}')
        print(f'cursor = {cursor}, next cursor = {cur_cursor}')
        print('---------------------------------------------------------')

        if (cur_cursor != cursor  and self.limit == 0) or len(self.tweets)<self.limit:
            self.start_request(cur_cursor)
        else:
            date_now = datetime.now().strftime("%H-%M-%S %d-%m-%Y")
            with open(self.settings.get('DATA_DIR') / f'query-{self.judul}-tweets.json', 'w') as outfile:
                json.dump(self.tweets, outfile)
            with open(self.settings.get('DATA_DIR') / f'query-{self.judul}-users.json', 'w') as outfile:
                json.dump(self.tweets, outfile)

parser = argparse.ArgumentParser(description='Script to get tweet from certain user.')
parser.add_argument("-q", "--query")
parser.add_argument("-u", "--username", default=None, type=str)
parser.add_argument("-l", "--limit", default=0, type=int)
parser.add_argument("-y", "--year", default=None, type=str)
parser.add_argument("-s", "--since", default=None, type=str)
parser.add_argument("-e", "--until", default=None, type=str)

args = parser.parse_args()

p = Search(args.query, args.username, args.limit, args.year, args.since, args.until)
p.start_request()

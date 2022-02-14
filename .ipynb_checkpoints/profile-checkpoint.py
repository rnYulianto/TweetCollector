import json
import requests
import argparse
from urllib.parse import quote, unquote

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from utils import get_cookies

def extract_cookies(selenium_cookies):
    cookies = {}
    for cookie in selenium_cookies:
        cookies[cookie['name']] = cookie['value']
    return cookies

def get_url(url, params):
    params_q = quote(json.dumps(params))
    return url + params_q

parser = argparse.ArgumentParser(description='Script to get tweet from certain user.')
parser.add_argument("-u", "--username", default="")
args = parser.parse_args()

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
    
if args.username == '':
    print('You need to specify the username')
    exit()
else:
    cookies, headers, userid, url_profile_token = get_cookies(args.username)
    url_params['userId'] = userid
    
r = requests.get(get_url(user_tweets_url.format(user_tweets_url_token=url_profile_token['userTweets']), url_params), headers=headers, cookies=extract_cookies(cookies))
    
print(r.text)
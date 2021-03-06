from utils.Settings import Settings
import os, logging
import json
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

def merge_dicts(*dict_args):
    """
    Given any number of dictionaries, shallow copy and merge into a new dict,
    precedence goes to key-value pairs in latter dictionaries.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

def get_settings():
    settings = Settings()
    return settings

def mkdirs(dirs):
    ''' Create `dirs` if not exist. '''
    if not os.path.exists(dirs):
        os.makedirs(dirs)

def process_browser_log_entry(entry):
    response = json.loads(entry['message'])['message']
    return response

def process_log_response_body(entry):
    response = json.loads(entry['body'])
    return response

def get_url_token(entry):
    url = entry['params']['response']['url']
    return url.split('/')[6]

def get_cookies(username = False, replies=False):
    caps = DesiredCapabilities.CHROME
    caps['goog:loggingPrefs'] = {'performance': 'ALL'}

    options = webdriver.ChromeOptions()
    options.binary_location = get_settings().get('BROWSER_PATH')

    driver = webdriver.Chrome(desired_capabilities=caps, options=options)
    
    if username:
        if replies:
            url = f'https://twitter.com/{username}/with_replies'
        else:
            url = f'https://twitter.com/{username}'
    else:
        # Visit random profile
        url = 'https://twitter.com/abc'
    driver.get(url)
    time.sleep(5)

    browser_log = driver.get_log('performance') 
    events = [process_browser_log_entry(entry) for entry in browser_log]

    ''' Extract cookies and token from received cookies '''
    cookies = None
    x_guest_token = ''
    headers = ''
    userid = ''
    url_profile_token = {}

    try:
        userByScreenName = [event for event in events if 'Network.response' in event['method'] and 'UserByScreenName' in event['params'].get('response', {}).get('url', '')][0]
        userTweets = [event for event in events if 'Network.response' in event['method'] and 'UserTweets' in event['params'].get('response', {}).get('url', '')][0]
        cookies = driver.get_cookies()
        x_guest_token = driver.get_cookie('gt')['value']
        # self.x_csrf_token = driver.get_cookie('ct0')['value']
        userByScreenName_response_body = process_log_response_body(driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': userByScreenName['params']['requestId']}))
        userid = userByScreenName_response_body['data']['user']['result']['rest_id']
        url_profile_token = {
            'userByScreenName': get_url_token(userByScreenName),
            'userTweets': get_url_token(userTweets)
        }
    except:
        logging.info('cookies are not updated!')

    driver.quit()

    headers = {
        'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
        'x-guest-token': x_guest_token,
        # 'x-csrf-token': self.x_csrf_token,
    }
    print('headers:\n--------------------------\n')
    print(headers)
    print('\n--------------------------\n')

    return cookies, headers, userid, url_profile_token

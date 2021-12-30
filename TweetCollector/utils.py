import os, logging

def mkdirs(dirs):
    ''' Create `dirs` if not exist. '''
    if not os.path.exists(dirs):
        os.makedirs(dirs)

def get_cookies(driver):
    ''' Extract cookies and token from received cookies '''
    cookies = None
    x_guest_token = ''
    headers = ''

    try:
        cookies = driver.get_cookies()
        x_guest_token = driver.get_cookie('gt')['value']
        # self.x_csrf_token = driver.get_cookie('ct0')['value']
    except:
        logging.info('cookies are not updated!')

    headers = {
        'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
        'x-guest-token': x_guest_token,
        # 'x-csrf-token': self.x_csrf_token,
    }
    print('headers:\n--------------------------\n')
    print(headers)
    print('\n--------------------------\n')

    return cookies, headers
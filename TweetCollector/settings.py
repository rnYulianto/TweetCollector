USER_AGENT = 'TweetCollector'

BOT_NAME = 'TweetCollector'
LOG_LEVEL = 'INFO'

SPIDER_MODULES = ['TweetCollector.spiders']
NEWSPIDER_MODULE = 'TweetCollector.spiders'
ITEM_PIPELINES = {
    'TweetCollector.pipelines.DuplicatesTweetPipeline': 100,
    'TweetCollector.pipelines.JsonLPipeline': 150,
}

SAVE_PATH = './data'

DOWNLOAD_DELAY = 1.0

# settings for selenium
from shutil import which
SELENIUM_DRIVER_NAME = 'chrome'
SELENIUM_BROWSER_EXECUTABLE_PATH = '' # Change to your browser path
SELENIUM_DRIVER_EXECUTABLE_PATH = '' # Change to your driver path
SELENIUM_DRIVER_ARGUMENTS = ''  # '--headless' if using chrome instead of firefox
DOWNLOADER_MIDDLEWARES = {
    'scrapy_selenium.SeleniumMiddleware': 800
}

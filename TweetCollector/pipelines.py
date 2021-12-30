import os, logging, json
from datetime import datetime

from scrapy import signals
from scrapy.utils.project import get_project_settings
from scrapy.exceptions import DropItem, CloseSpider
from scrapy.exporters import JsonLinesItemExporter

from TweetCollector.items import Tweet, User
from TweetCollector.utils import mkdirs

SETTINGS = get_project_settings()

class DuplicatesTweetPipeline(object):
    def __init__(self):
        self.saved_tweet = set()
        self.saved_user = set()
    
    def process_item(self, item, spider):
        if isinstance(item, Tweet):
            if item['id_'] in self.saved_tweet:
                logging.warning(f'Tweet dropped due duplications: {item["id_"]}')
                raise DropItem(item)
            else:
                self.saved_tweet.add(item['id_'])
                return item
        elif isinstance(item, User):
            if item['id_'] in self.saved_user:
                logging.warning(f'User dropped due duplications: {item["id_"]}')
                raise DropItem(item)
            else:
                self.saved_user.add(item['id_'])
                return item
        else:
            return item

class JsonLPipeline(object):
    def __init__(self):
        self.savePath = SETTINGS['SAVE_PATH']
        mkdirs(self.savePath)
        self.limit = 0
        self.num_saved_tweet = 0

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        date_now = datetime.now().strftime("%H-%M-%S %d-%m-%Y")

        self.tweet_file = open(f'data/tweet - {date_now}.jsonl', 'w+b')
        self.tweet_exporter = JsonLinesItemExporter(self.tweet_file)
        self.tweet_exporter.start_exporting()

        self.user_file = open(f'data/user - {date_now}.jsonl', 'w+b')
        self.user_exporter = JsonLinesItemExporter(self.user_file)
        self.user_exporter.start_exporting()

    def spider_closed(self, spider):
        self.tweet_exporter.finish_exporting()
        self.tweet_file.close()

        self.user_exporter.finish_exporting()
        self.user_file.close()

    def process_item(self, item, spider):
        self.limit = spider.limit
        
        if isinstance(item, Tweet):
            print(f'Export Tweet: {item["id_"]}')
            self.num_saved_tweet += 1
            self.tweet_exporter.export_item(item)
            if (self.num_saved_tweet == self.limit) and (self.limit != 0):
                spider.at_limit = True
                print('NEED TO CLOSE')

        if isinstance(item, User):
            print(f'Export User: {item["id_"]}')
            self.user_exporter.export_item(item)

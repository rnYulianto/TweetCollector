from scrapy import Item, Field


class Tweet(Item):
    id_ = Field()
    tweet = Field()

class User(Item):
    id_ = Field()
    user = Field()

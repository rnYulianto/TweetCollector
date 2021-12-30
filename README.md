# Introduction #
`TweetCollector` can get tweets from [Twitter Search](https://twitter.com/explore). 
It is built on [Scrapy](http://scrapy.org/).

# Depedency #
1. [Scrapy](http://scrapy.org/)
2. [scrapy-selenium](https://github.com/clemfromspace/scrapy-selenium)


# Usage #

1. Change the `USER_AGENT` in `TweetCollector/settings.py` to identify who you are
	
		USER_AGENT = 'your website/e-mail'

2. In the root folder of this project, run command: 

		scrapy crawl search -a query="something"

3. You can also use helper parameter
    - limit, to limit the tweet collected
    - year, to search on certain year
    - since, when the tweet started collected (YYYY-MM-dd)
    - until, date where tweet last collected (YYYY-MM-dd)
            
            scrapy crawl search -a query="something" -a limit=50 -a year=2020

4. The tweets will be saved to disk in `./data/` in default settings with format of Json Line. Change the `SAVE_PATH` in `TweetCollector/settings.py` if you want another location.
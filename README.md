# Introduction #
`TweetCollector` can get tweets from [Twitter Search](https://twitter.com/explore) and User Profile.

# Depedency #
1. [python >= 3.7.*](https://www.python.org/)
1. [Requests](https://docs.python-requests.org/en/latest/)
1. [Selenium](https://selenium-python.readthedocs.io/)


# Usage #

1. This scraper only work with chronium based browser for now
1. Change the `BROWSER_PATH` in `utils\setting_files\settings.py` to where your browser .exe file

1. For search tweet using query, in the root folder of this project, run command: 

		python search.py -q query

1. You can also use helper parameter
    - username (`-u` or `--username`), to get tweet from certain user
    - limit (`-l` or `--limit`), to limit the tweet collected
    - year (`-y` or `year`), to search on certain year
    - since (`-s` or `since`), when the tweet started collected (YYYY-MM-dd)
    - until (`-e` or `until`), date where tweet last collected (YYYY-MM-dd)
            
            python search.py -q query -l 50 --year 2022

1. The tweets will be saved to disk in `data/` in default settings with format of Json. Change the `DATA_DIR` in `utils\setting_files\settings.py` if you want another location.

1. You can also get tweets from certain username (limit are the only option available in this function) with command:

        python profile.py -u username

1. You can also get tweets from certain username with replies (limit are the only option available in this function) with command:

        python profile_with_replies.py -u username

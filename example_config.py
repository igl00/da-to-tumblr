""" Fll in the missing information and rename this file to config.py to get started.
"""
import logging

DA_RSS_FEED_URL = ''  # An rss feed from Deviant Art containing images
TUMBLR_BLOG_URL = ''  # The Tumblr blog to post the images to

FEED_STATE = 'rss_tracker.txt'  # A file that keeps track of posted items

LOG_TO_FILE = True
LOG_TO_CONSOLE = True
CONSOLE_LOG_LEVEL = logging.INFO
FILE_LOG_LEVEL = logging.INFO
LOG_FILE = 'log.txt'

POST_STATE = 'published'  # options are: published, draft, queue, private

THROTTLE_API_POSTS = True
MEAN_WAIT_TIME = 0.9  # seconds
WAIT_TIME_SPREAD = 1  # seconds


# Tumblr API Keys
# To acquire a key visit: https://www.tumblr.com/oauth/apps
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
TOKEN_KEY = ''
TOKEN_SECRET = ''


""" Post any items in a given Deviant Art rss feed to a Tumblr blog.
    Limited to the most recent 60 items in most cases by the Deviant Art rss feeds.
"""
import feedparser
import random
import os
from tumblpy import Tumblpy, TumblpyError
from config import *
from time import sleep


client = Tumblpy(CONSUMER_KEY, CONSUMER_SECRET, TOKEN_KEY, TOKEN_SECRET)
STATE_DIR = os.path.join(os.path.curdir, 'state')
FEED_STATE = os.path.join(STATE_DIR, FEED_STATE)

logger = logging.getLogger('da-to-tumblr')
logger.setLevel(min(FILE_LOG_LEVEL, CONSOLE_LOG_LEVEL))
log_formatter = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s', '%Y-%m-%d %H:%M:%S')

# Create the folder for the state file if it doesn't exist
if not os.path.exists(STATE_DIR):
    os.mkdir(STATE_DIR)

if LOG_TO_CONSOLE:
    console_log = logging.StreamHandler()
    console_log.setLevel(logging.DEBUG)
    console_log.setFormatter(log_formatter)
    logger.addHandler(console_log)

if LOG_TO_FILE:
    # Create the folder for the log if it doesn't exist
    log_dir = os.path.join(os.path.curdir, 'logs')
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    # Configure the logging file
    log_file = logging.FileHandler(os.path.join(log_dir, LOG_FILE))
    log_file.setLevel(FILE_LOG_LEVEL)
    log_file.setFormatter(log_formatter)
    logger.addHandler(log_file)


class PostError(Exception):
    pass


def publish_item(item):
    """ Post the given item to tumblr.
        Raises a TumblpyError is something goes wrong with the post api call.
    """
    item_id = int(item['id'].split('-')[-1])
    image_title = item['title']
    image_source = item['media_content'][0]['url']
    image_page = item['link']
    artist = item['media_credit'][0]['content']
    artist_page = item['media_copyright']['url']

    caption = '<a href="{0}">{1}</a> by <a href="{2}">{3}<a>'.format(image_page, image_title, artist_page, artist)

    logger.info('Publishing<{0}>: {1}'.format(item_id, item['title']))

    try:
        client.post('post', blog_url=TUMBLR_BLOG_URL, params={'type': 'photo',
                                                              'state': POST_STATE,
                                                              'caption': caption,
                                                              'source': image_source,
                                                              'link': image_page})
    except TumblpyError as error:
        logger.error('<{0}> CODE: {1} MESSAGE: {2}'.format(item_id, error.error_code, error.msg))
        logger.debug('Caption: "{0}"\nSource: "{1}"\nLink: "{2}"\n'.format(caption, image_source, image_page))
        raise PostError(error.msg)

    # Log the results
    logger.info('Image source: "{}"'.format(image_source))
    logger.info('Image page: "{}"'.format(image_page))
    logger.info('Image title: "{}"'.format(image_title))
    logger.info('Artist: "{}"'.format(artist))
    logger.info('Artist\'s Page: "{}"'.format(artist_page))
    logger.info('=' * 20)


def main():
    feed = feedparser.parse(DA_RSS_FEED_URL)
    with open(FEED_STATE, 'r') as file:
        published_items = [int(line.strip()) for line in file.readlines()]

    for item in reversed(feed.entries):
        item_id = int(item['id'].split('-')[-1])
        if item_id not in published_items:
            try:
                publish_item(item)
                with open(FEED_STATE, 'a') as file:
                    file.write(str(item_id) + '\n')
            except PostError:
                logger.error('Error publishing: {}'.format(item_id))
            finally:
                if THROTTLE_API_POSTS:
                    sleep(MEAN_WAIT_TIME + random.uniform(-(WAIT_TIME_SPREAD / 2), WAIT_TIME_SPREAD / 2))


if __name__ == '__main__':
    main()
    if LOG_TO_CONSOLE:
        input('Press enter to close...')

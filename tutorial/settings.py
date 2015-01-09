# -*- coding: utf-8 -*-

# Scrapy settings for tutorial project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'pastthepost'

SPIDER_MODULES = ['tutorial.spiders']
NEWSPIDER_MODULE = 'tutorial.spiders'
DUPEFILTER_DEBUG = False

# #dfo to bfo
# DEPTH_PRIORITY = 1
# SCHEDULER_DISK_QUEUE = 'scrapy.squeue.PickleFifoDiskQueue'
# SCHEDULER_MEMORY_QUEUE = 'scrapy.squeue.FifoMemoryQueue'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Googlebot/2.1 (+http://www.googlebot.com/bot.html)'

#this is a dictionary
ITEM_PIPELINES = {'scrapy.contrib.pipeline.images.ImagesPipeline': 1, 'tutorial.pipelines.HKDBPipeline':2}
IMAGES_STORE = '/users/vmac/Documents/programming/PY/scrapy/tutorial/images'
FILES_STORE = '/users/vmac/Documents/programming/PY/scrapy/tutorial/videos'


DATABASE = {'drivername': 'postgres',
            'host': 'localhost',
            'port': '5432',
            'username': 'vmac',
            'password': '',
            'database': 'hkraces'}

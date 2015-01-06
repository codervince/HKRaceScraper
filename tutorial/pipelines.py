# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem


class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item

# class MyImagesPipeline(ImagesPipeline):

# 	def get_media_requests(self, item, info):
# 		for image_url in item['image_urls']:
# 			print item.get('image_urls', [])
# 			yield scrapy.Request(image_url)



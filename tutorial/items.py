# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HKResultItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Url = scrapy.Field()
    RaceNumber = scrapy.Field()
    RaceIndex = scrapy.Field()
    Place = scrapy.Field()
    HorseNo = scrapy.Field()
    Horse = scrapy.Field()
    HorseCode = scrapy.Field()
    Jockey = scrapy.Field()
    Trainer = scrapy.Field()
    ActualWt = scrapy.Field()
    DeclarHorseWt = scrapy.Field()
    Draw = scrapy.Field()
    LBW = scrapy.Field()
    RunningPosition = scrapy.Field()
    FinishTime = scrapy.Field()
    WinOdds = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()

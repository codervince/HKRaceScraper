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
    Racecoursecode = scrapy.Field()
    Racedate = scrapy.Field()
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
    # image_urls = scrapy.Field()
    # images = scrapy.Field()
    WinDiv = scrapy.Field()
    IncidentReport = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    #used to match up data from 2 pages
    # SecPlace = scrapy.Field()
    # SecHorseNo = scrapy.Field()
    # SecHorseName = scrapy.Field()
    ###############
    Sec1DBL = scrapy.Field()
    Sec1Time = scrapy.Field()
    Sec2DBL = scrapy.Field()
    Sec2Time = scrapy.Field()
    Sec3DBL = scrapy.Field()
    Sec3Time = scrapy.Field()
    Sec4DBL = scrapy.Field()
    Sec4Time = scrapy.Field()
    Sec5DBL = scrapy.Field()
    Sec5Time = scrapy.Field()
    Sec6DBL = scrapy.Field()
    Sec6Time = scrapy.Field()
    HorseReport = scrapy.Field()
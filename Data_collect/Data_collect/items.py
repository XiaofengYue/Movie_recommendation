# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DataCollectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ID = scrapy.Field()
    title = scrapy.Field()
    pubdates = scrapy.Field()
    durations = scrapy.Field()
    genres = scrapy.Field()
    countries = scrapy.Field()
    image = scrapy.Field()
    summary = scrapy.Field()
    directors = scrapy.Field()
    casts = scrapy.Field()

    star_five = scrapy.Field()
    star_four = scrapy.Field()
    star_three = scrapy.Field()
    star_two = scrapy.Field()
    star_one = scrapy.Field()

class UserItem(scrapy.Item):
    ID = scrapy.Field()
    name = scrapy.Field()
    genres = scrapy.Field()
    image = scrapy.Field()
    time = scrapy.Field()

class RateItem(scrapy.Item):
    user_id = scrapy.Field()
    movie_id = scrapy.Field()
    star = scrapy.Field()
# -*- coding: UTF-8 -*-
import scrapy
import json
from Data_collect.items import DataCollectItem

class All_Movies(scrapy.spiders.Spider):
    name = 'all_movies'
    start_urls = [
        "https://douban.uieee.com/v2/movie/subject/1764796"
    ]

    def parse(self, response):
        

        # 抓取的json
        content = json.loads(response.body_as_unicode())

        item = DataCollectItem()
        item['ID'] = int(content['id'])
        item['title'] = content['title']
        if type(content['pubdates']) is list:
            content['pubdates'] = "".join(content['pubdates'])
        item['pubdates'] = content['pubdates']

        if type(content['durations']) is list:
            content['durations'] = "".join(content['durations'])
        item['durations'] = content['durations']

        if type(content['genres']) is list:
            content['genres'] = "".join(content['genres'])
        item['genres'] = content['genres']

        if type(content['countries']) is list:
            content['countries'] = "".join(content['countries'])
        item['countries'] = content['countries']
        item['image'] = content['images']['small']
        item['summary'] = content['summary'].replace('\n','').replace('\r','').replace('\r\n','')
        yield item
        
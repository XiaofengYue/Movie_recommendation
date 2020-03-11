# -*- coding: UTF-8 -*-
import scrapy
import json,os,configparser
from Data_collect.items import DataCollectItem

class All_Movies(scrapy.spiders.Spider):
    name = 'all_movies'
    #加载配置文件
    conf = configparser.ConfigParser()
    CONFIG_FILE = 'scrapy.cfg'
    if os.path.exists( os.path.join( os.getcwd(),CONFIG_FILE ) ):
        conf.read(CONFIG_FILE)

        #根据文件中的ID爬取数据
        num = int(conf.get("movies","txt_number"))
        with open("ID/"+str(num)+'.txt') as f:
            li = f.read().split('\n')
            start_urls = ["https://douban.uieee.com/v2/movie/subject/"+str(i) for i in li]

        # 根据ID递增爬取
        # s_id = int(conf.get("movies","end_id"))
        # distance = int(conf.get("movies","distance_id"))
        # start_urls = ["https://douban.uieee.com/v2/movie/subject/"+str(i) for i in range(s_id,s_id+distance)]
        
        # with open(CONFIG_FILE,'w') as f:
        #     conf.set("movies","start_id",str(s_id))
        #     conf.set("movies","end_id",str(s_id+distance))
        #     conf.write(f)
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
            content['genres'] = ",".join(content['genres'])
        item['genres'] = content['genres']

        if type(content['countries']) is list:
            content['countries'] = "".join(content['countries'])
        item['countries'] = content['countries']
        item['image'] = content['images']['small']
        item['summary'] = content['summary'].replace('\n','').replace('\r','').replace('\r\n','')
        item['star_five'] = int(content['rating']['details']['5'])
        item['star_four'] = int(content['rating']['details']['4'])
        item['star_three'] = int(content['rating']['details']['3'])
        item['star_two'] = int(content['rating']['details']['2'])
        item['star_one'] = int(content['rating']['details']['1'])
        yield item
        
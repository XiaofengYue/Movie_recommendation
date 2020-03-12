# -*- coding: UTF-8 -*-
import scrapy
import json,os,configparser,time
from Data_collect.items import DataCollectItem


class test_ip(scrapy.spiders.Spider):
    name = 'ip'
    allowed_domains = ['httpbin.org']
    start_urls = ['https://httpbin.org/ip']

    def parse(self, response):
        origin = json.loads(response.text)['origin']
        print(origin)
        yield scrapy.Request(self.start_urls[0])

class Movie_ID(scrapy.spiders.Spider):
    name = 'movie_id'


    def start_requests(self):
        tags = ['电影','电视剧','综艺','动漫','纪录片','短片']
        genres = ['剧情','喜剧','动作','爱情','科幻','动画','悬疑','惊悚','恐怖','犯罪','同性','音乐','歌舞','传记','历史','战争','西部','奇幻','冒险','灾难','武侠','情色']
        genres = ['剧情']
        countries = ['中国大陆','美国','中国香港','中国台湾','日本','韩国','英国','法国','德国','意大利','西班牙','印度','泰国','俄罗斯','伊朗','加拿大','澳大利亚','爱尔兰','瑞典','巴西','丹麦']
        dic_ = {"情色":600,"剧情":10000}
        for self.genre in genres:
            for self.country in countries:
                for self.start in range(0,10000,20):
                    url = 'https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags={}&start={}&genres={}&countries={}'.format('电影',str(self.start),self.genre,self.country)
                    yield scrapy.Request(url,callback=self.getinfo)
        
        # self.start=0
        # for i in range(0,100,20):
        #     url = 'https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=%E7%94%B5%E5%BD%B1&start={}&genres=%E6%83%85%E8%89%B2&countries=%E4%B8%AD%E5%9B%BD%E5%A4%A7%E9%99%86'.format(str(i))
        #     yield scrapy.Request(url,callback=self.getinfo)

    def getinfo(self, response):
        content = json.loads(response.body_as_unicode())

        if 'data' in content:
            data = content['data']
            for info in data:
                item = DataCollectItem()
                item['ID'] = int(info['id'])
                item['title'] = info['title']
                item['casts'] = ",".join(info['casts'])
                item['directors'] = ",".join(info['directors'])
                yield item
        else:
            print(content)
            print("genre:{},contry:{},start:{}".format(self.genre,self.country,self.start))
            with open('err.log','a') as f:
                msg = content + "genre:{},contry:{},start:{}\n".format(self.genre,self.country,self.start)
                f.write(msg)
            time.sleep(3)
            yield scrapy.Request(response.url,callback=self.getinfo)
            # time.sleep(3600*3)




class All_Movies(scrapy.spiders.Spider):
    name = 'all_movies'
    #加载配置文件
    conf = configparser.ConfigParser()
    CONFIG_FILE = 'scrapy.cfg'
    if os.path.exists( os.path.join( os.getcwd(),CONFIG_FILE ) ):
        conf.read(CONFIG_FILE)

        #根据文件中的ID爬取数据
        # num = int(conf.get("movies","txt_number"))
        # with open("ID/"+str(num)+'.txt') as f:
        #     li = f.read().split('\n')
        #     start_urls = ["https://douban.uieee.com/v2/movie/subject/"+str(i) for i in li]

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
        
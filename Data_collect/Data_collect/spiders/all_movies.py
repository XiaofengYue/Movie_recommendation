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

        self.cookies={'cookie':'douban-fav-remind=1; douban-profile-remind=1; _vwo_uuid_v2=D4BEEC156A416D3DBF7DCEC30CD6EEF09|e36d57937d07928f12b3f112e162573f; gr_user_id=c702c0f7-31ab-44d4-8ca4-2193f6b4a7a3; bid=_IQuumecNtk; viewed="19970032_30236304_6798611_3674537_5299764_5252677_26927702_30140436_26163454_1102259"; ll="108310"; push_noty_num=0; push_doumail_num=0; __utmv=30149280.12160; __utmc=30149280; dbcl2="121600284:9iGbJa0EuZU"; ck=HxYc; __utmz=30149280.1583909870.11.7.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1584075389%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DGePqGTgQy3ge1-KtAT6jt6Zk5ZoEX8_O2Iah0NPfxNpyG_yACFr_lkLfk5AHhXOamXY2IZbGxqEVq0NgqXtpWK%26wd%3D%26eqid%3Dd36919e70006461d000000035e6614b7%22%5D; _pk_ses.100001.8cb4=*; ap_v=0,6.0; __utma=30149280.1830171042.1583331055.1584002571.1584075389.14; __utmt=1; __utmb=30149280.2.10.1584075389; _pk_id.100001.8cb4=d247c006175a3b1e.1535352166.29.1584075393.1584002579.'}
        d = {
            '剧情':{'中国大陆':10000,'美国':10000,'中国香港':3750,'中国台湾':2750,'日本':10000,'韩国':3500,'英国':10000,'法国':1000,'德国':1000,'意大利':1000,'西班牙':1000,'印度':1000,'泰国':1000,'俄罗斯':1000,'伊朗':1000,'加拿大':1000,'澳大利亚':1000,'爱尔兰':1000,'瑞典':1000,'巴西':1000,'丹麦':1000},
            '喜剧':{'中国大陆':10000,'美国':10000,'中国香港':3750,'中国台湾':2750,'日本':10000,'韩国':3500,'英国':10000,'法国':1000,'德国':1000,'意大利':1000,'西班牙':1000,'印度':1000,'泰国':1000,'俄罗斯':1000,'伊朗':1000,'加拿大':1000,'澳大利亚':1000,'爱尔兰':1000,'瑞典':1000,'巴西':1000,'丹麦':1000},
            '动作':{'中国大陆':10000,'美国':10000,'中国香港':3750,'中国台湾':2750,'日本':10000,'韩国':3500,'英国':10000,'法国':1000,'德国':1000,'意大利':1000,'西班牙':1000,'印度':1000,'泰国':1000,'俄罗斯':1000,'伊朗':1000,'加拿大':1000,'澳大利亚':1000,'爱尔兰':1000,'瑞典':1000,'巴西':1000,'丹麦':1000},
            '爱情':{'中国大陆':10000,'美国':10000,'中国香港':3750,'中国台湾':2750,'日本':10000,'韩国':3500,'英国':10000,'法国':1000,'德国':1000,'意大利':1000,'西班牙':1000,'印度':1000,'泰国':1000,'俄罗斯':1000,'伊朗':1000,'加拿大':1000,'澳大利亚':1000,'爱尔兰':1000,'瑞典':1000,'巴西':1000,'丹麦':1000},
            '科幻':{'中国大陆':10000,'美国':10000,'中国香港':3750,'中国台湾':2750,'日本':10000,'韩国':3500,'英国':10000,'法国':1000,'德国':1000,'意大利':1000,'西班牙':1000,'印度':1000,'泰国':1000,'俄罗斯':1000,'伊朗':1000,'加拿大':1000,'澳大利亚':1000,'爱尔兰':1000,'瑞典':1000,'巴西':1000,'丹麦':1000},
            '动画':{'中国大陆':10000,'美国':10000,'中国香港':3750,'中国台湾':2750,'日本':10000,'韩国':3500,'英国':10000,'法国':1000,'德国':1000,'意大利':1000,'西班牙':1000,'印度':1000,'泰国':1000,'俄罗斯':1000,'伊朗':1000,'加拿大':1000,'澳大利亚':1000,'爱尔兰':1000,'瑞典':1000,'巴西':1000,'丹麦':1000},
            '悬疑':{'中国大陆':10000,'美国':10000,'中国香港':3750,'中国台湾':2750,'日本':10000,'韩国':3500,'英国':10000,'法国':1000,'德国':1000,'意大利':1000,'西班牙':1000,'印度':1000,'泰国':1000,'俄罗斯':1000,'伊朗':1000,'加拿大':1000,'澳大利亚':1000,'爱尔兰':1000,'瑞典':1000,'巴西':1000,'丹麦':1000},
            '惊悚':{'中国大陆':10000,'美国':10000,'中国香港':3750,'中国台湾':2750,'日本':10000,'韩国':3500,'英国':10000,'法国':1000,'德国':1000,'意大利':1000,'西班牙':1000,'印度':1000,'泰国':1000,'俄罗斯':1000,'伊朗':1000,'加拿大':1000,'澳大利亚':1000,'爱尔兰':1000,'瑞典':1000,'巴西':1000,'丹麦':1000},
            '恐怖':{'中国大陆':10000,'美国':10000,'中国香港':3750,'中国台湾':2750,'日本':10000,'韩国':3500,'英国':10000,'法国':1000,'德国':1000,'意大利':1000,'西班牙':1000,'印度':1000,'泰国':1000,'俄罗斯':1000,'伊朗':1000,'加拿大':1000,'澳大利亚':1000,'爱尔兰':1000,'瑞典':1000,'巴西':1000,'丹麦':1000},
            '犯罪':{'中国大陆':1000,'美国':10000,'中国香港':3750,'中国台湾':2750,'日本':10000,'韩国':3500,'英国':10000,'法国':1000,'德国':1000,'意大利':1000,'西班牙':1000,'印度':1000,'泰国':1000,'俄罗斯':1000,'伊朗':1000,'加拿大':1000,'澳大利亚':1000,'爱尔兰':1000,'瑞典':1000,'巴西':1000,'丹麦':1000},
            '同性':{'中国大陆':1000,'美国':10000,'中国香港':3750,'中国台湾':2750,'日本':10000,'韩国':3500,'英国':10000,'法国':1000,'德国':1000,'意大利':1000,'西班牙':1000,'印度':1000,'泰国':1000,'俄罗斯':1000,'伊朗':1000,'加拿大':1000,'澳大利亚':1000,'爱尔兰':1000,'瑞典':1000,'巴西':1000,'丹麦':1000},
            '音乐':{'中国大陆':1000,'美国':10000,'中国香港':3750,'中国台湾':2750,'日本':10000,'韩国':3500,'英国':10000,'法国':1000,'德国':1000,'意大利':1000,'西班牙':1000,'印度':1000,'泰国':1000,'俄罗斯':1000,'伊朗':1000,'加拿大':1000,'澳大利亚':1000,'爱尔兰':1000,'瑞典':1000,'巴西':1000,'丹麦':1000},
            '歌舞':{'中国大陆':1000,'美国':10000,'中国香港':3750,'中国台湾':2750,'日本':10000,'韩国':3500,'英国':10000,'法国':1000,'德国':1000,'意大利':1000,'西班牙':1000,'印度':1000,'泰国':1000,'俄罗斯':1000,'伊朗':1000,'加拿大':1000,'澳大利亚':1000,'爱尔兰':1000,'瑞典':1000,'巴西':1000,'丹麦':1000},
            '传记':{'中国大陆':1000,'美国':10000,'中国香港':3750,'中国台湾':2750,'日本':10000,'韩国':3500,'英国':10000,'法国':1000,'德国':1000,'意大利':1000,'西班牙':1000,'印度':1000,'泰国':1000,'俄罗斯':1000,'伊朗':1000,'加拿大':1000,'澳大利亚':1000,'爱尔兰':1000,'瑞典':1000,'巴西':1000,'丹麦':1000},
            '历史':{'中国大陆':10000,'美国':10000,'中国香港':3750,'中国台湾':2750,'日本':10000,'韩国':3500,'英国':10000,'法国':1000,'德国':1000,'意大利':1000,'西班牙':1000,'印度':1000,'泰国':1000,'俄罗斯':1000,'伊朗':1000,'加拿大':1000,'澳大利亚':1000,'爱尔兰':1000,'瑞典':1000,'巴西':1000,'丹麦':1000},
            '战争':{'中国大陆':10000,'美国':10000,'中国香港':3750,'中国台湾':2750,'日本':10000,'韩国':3500,'英国':10000,'法国':1000,'德国':1000,'意大利':1000,'西班牙':1000,'印度':1000,'泰国':1000,'俄罗斯':1000,'伊朗':1000,'加拿大':1000,'澳大利亚':1000,'爱尔兰':1000,'瑞典':1000,'巴西':1000,'丹麦':1000},
            '西部':{'中国大陆':1000,'美国':10000,'中国香港':3750,'中国台湾':2750,'日本':10000,'韩国':3500,'英国':10000,'法国':1000,'德国':1000,'意大利':1000,'西班牙':1000,'印度':1000,'泰国':1000,'俄罗斯':1000,'伊朗':1000,'加拿大':1000,'澳大利亚':1000,'爱尔兰':1000,'瑞典':1000,'巴西':1000,'丹麦':1000},
            '奇幻':{'中国大陆':1000,'美国':10000,'中国香港':3750,'中国台湾':2750,'日本':10000,'韩国':3500,'英国':10000,'法国':1000,'德国':1000,'意大利':1000,'西班牙':1000,'印度':1000,'泰国':1000,'俄罗斯':1000,'伊朗':1000,'加拿大':1000,'澳大利亚':1000,'爱尔兰':1000,'瑞典':1000,'巴西':1000,'丹麦':1000},
            '冒险':{'中国大陆':1000,'美国':10000,'中国香港':3750,'中国台湾':2750,'日本':10000,'韩国':3500,'英国':10000,'法国':1000,'德国':1000,'意大利':1000,'西班牙':1000,'印度':1000,'泰国':1000,'俄罗斯':1000,'伊朗':1000,'加拿大':1000,'澳大利亚':1000,'爱尔兰':1000,'瑞典':1000,'巴西':1000,'丹麦':1000},
            '灾难':{'中国大陆':1000,'美国':10000,'中国香港':3750,'中国台湾':2750,'日本':10000,'韩国':3500,'英国':10000,'法国':1000,'德国':1000,'意大利':1000,'西班牙':1000,'印度':1000,'泰国':1000,'俄罗斯':1000,'伊朗':1000,'加拿大':1000,'澳大利亚':1000,'爱尔兰':1000,'瑞典':1000,'巴西':1000,'丹麦':1000},
            '武侠':{'中国大陆':10000,'美国':10000,'中国香港':3750,'中国台湾':2750,'日本':10000,'韩国':3500,'英国':10000,'法国':1000,'德国':1000,'意大利':1000,'西班牙':1000,'印度':1000,'泰国':1000,'俄罗斯':1000,'伊朗':1000,'加拿大':1000,'澳大利亚':1000,'爱尔兰':1000,'瑞典':1000,'巴西':1000,'丹麦':1000},
            '情色':{'中国大陆':1000,'美国':10000,'中国香港':3750,'中国台湾':2750,'日本':10000,'韩国':3500,'英国':10000,'法国':1000,'德国':1000,'意大利':1000,'西班牙':1000,'印度':1000,'泰国':1000,'俄罗斯':1000,'伊朗':1000,'加拿大':1000,'澳大利亚':1000,'爱尔兰':1000,'瑞典':1000,'巴西':1000,'丹麦':1000},
        }


        genres = ['剧情','喜剧','动作','爱情','科幻','动画','悬疑','惊悚','恐怖','犯罪','同性','音乐','歌舞','传记','历史','战争','西部','奇幻','冒险','灾难','武侠','情色']
        countries = ['中国大陆','美国','中国香港','中国台湾','日本','韩国','英国','法国','德国','意大利','西班牙','印度','泰国','俄罗斯','伊朗','加拿大','澳大利亚','爱尔兰','瑞典','巴西','丹麦']

        # for self.genre in genres:
        #     for self.country in countries:
        #         for self.start in range(0,10000,20):
        #             url = 'https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags={}&start={}&genres={}&countries={}'.format('电影',str(self.start),self.genre,self.country)
        #             yield scrapy.Request(url,callback=self.getinfo)
        
        self.genre = '剧情'
        for self.country in countries:
            for self.start in range(0,d[self.genre][self.country],20):
                url = 'https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags={}&start={}&genres={}&countries={}'.format('电影',str(self.start),self.genre,self.country)
                yield scrapy.Request(url,callback=self.getinfo,cookies=self.cookies)


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
                #msg = content + "genre:{},contry:{},start:{}\n".format(self.genre,self.country,self.start)
                f.write(str(time.asctime( time.localtime(time.time()) )))
                msg = "\n" + str(content)+"contry:"+str(self.country)+"start:"+str(self.start)+"\n"
                f.write(msg)
            # time.sleep(60*60)
            yield scrapy.Request(response.url,callback=self.getinfo,cookies=self.cookies)
            # time.sleep(3600*3)




class All_Movies(scrapy.spiders.Spider):
    name = 'all_movies'
    #加载配置文件
    conf = configparser.ConfigParser()
    CONFIG_FILE = 'scrapy.cfg'
    if os.path.exists( os.path.join( os.getcwd(),CONFIG_FILE ) ):
        conf.read(CONFIG_FILE)

        #根据文件中的ID爬取数据
        num = int(conf.get("movies","txt_number"))
        for num_i in range(1,num):
            with open("ID/"+str(num_i)+'.txt') as f:
                li = f.read().split('\n')
                start_urls = ["https://douban.uieee.com/v2/movie/subject/"+str(i) for i in li]

        #根据ID递增爬取
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

        item['pubdates'] = ",".join(content['pubdates'])

        item['durations'] = ",".join(content['durations'])

        item['genres'] = ",".join(content['genres'])

        item['countries'] = ",".join(content['countries'])

        # item['directors'] = ",".join(content['directors'])
        # item['casts'] = ",".join(content['casts'])

        item['image'] = content['images']['small']
        item['summary'] = content['summary'].replace('\n','').replace('\r','').replace('\r\n','')
        item['star_five'] = int(content['rating']['details']['5'])
        item['star_four'] = int(content['rating']['details']['4'])
        item['star_three'] = int(content['rating']['details']['3'])
        item['star_two'] = int(content['rating']['details']['2'])
        item['star_one'] = int(content['rating']['details']['1'])
        yield item
        
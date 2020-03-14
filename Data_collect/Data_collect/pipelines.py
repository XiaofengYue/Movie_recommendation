# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql,time

class DataCollectPipeline(object):

    def __init__(self, settings):
        self.settings = settings
        self.SQLInsert = '''
            insert into info(id,title,pubdates,durations,genres,countries,image,summary,star_five,star_four,star_three,star_two,star_one)
            values('{id}','{title}','{pubdates}','{durations}','{genres}','{countries}','{image}','{summary}','{star_five}','{star_four}','{star_three}','{star_two}','{star_one}')
        '''
        self.idInsert = '''
            insert into info(id,title,casts,directors)
            values('{id}','{title}','{casts}','{directors}')
        '''
        self.userInset = '''
            insert into user(time,id,image,name)
            values('{time}','{id}','{image}','{name}')
        '''
        self.rateInset = '''
            insert into rate(user_id,movie_id,star)
            values('{user_id}','{movie_id}','{star}')
        '''

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def open_spider(self, spider):
        # 连接数据库
        self.connect = pymysql.connect(
            host=self.settings.get('MYSQL_HOST'),
            port=self.settings.get('MYSQL_PORT'),
            db=self.settings.get('MYSQL_DBNAME'),
            user=self.settings.get('MYSQL_USER'),
            passwd=self.settings.get('MYSQL_PASSWD'),
            charset='utf8',
            use_unicode=True
        )
        self.cursor = self.connect.cursor()
        self.connect.autocommit(True)
    
    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()

    def process_item(self, item, spider):

        if spider.name == 'rate':
            # print(item['user_id'])
            # print(item['movie_id'])
            # print(item['star'])
            sqltext = self.rateInset.format(
                user_id = pymysql.escape_string(item['user_id']),
                movie_id = item['movie_id'],
                star = item['star']
            )

        if spider.name == "user":
            sqltext = self.userInset.format(
                time=pymysql.escape_string(item['time']),
                id = pymysql.escape_string(item['ID']),
                image = pymysql.escape_string(item['image']),
                name = pymysql.escape_string(item['name'])
            )

        if spider.name == "movie_id":
            sqltext = self.idInsert.format(
                id=item['ID'],
                title=pymysql.escape_string(item['title']),
                casts=pymysql.escape_string(item['casts']),
                directors=pymysql.escape_string(item['directors']),
            )

        if spider.name == "all_movies":
            sqltext = self.SQLInsert.format(
                id=item['ID'],
                title=pymysql.escape_string(item['title']),
                pubdates=pymysql.escape_string(item['pubdates']),
                durations=pymysql.escape_string(item['durations']),
                genres=pymysql.escape_string(item['genres']),
                countries=pymysql.escape_string(item['countries']),
                image=pymysql.escape_string(item['image']),
                summary=pymysql.escape_string(item['summary']),
                star_five=item['star_five'],
                star_four=item['star_four'],
                star_three=item['star_three'],
                star_two=item['star_two'],
                star_one=item['star_one'])

        self.cursor.execute(sqltext)
        # try:
        #    self.cursor.execute(sqltext)
        # except pymysql.err.IntegrityError as f:
        #     pass
        #     with open('err.log','a') as f:
        #         f.write(str(time.asctime( time.localtime(time.time()) )))
        #         f.write('\npymysql插入错误,错误ID:' + str(item['ID'])+',错误信息:'+str(f) +'\n')
        # else:
        #     with open('err.log','a') as f:
        #         f.write(str(time.asctime( time.localtime(time.time()) )))
        #         f.write('\npymysql未知错误,错误ID:'+str(item['ID'])+',错误信息:'+str(f) +'\n')
            
        return item

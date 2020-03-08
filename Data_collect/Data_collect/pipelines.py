# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql


class DataCollectPipeline(object):

    def __init__(self, settings):
        self.settings = settings
        self.SQLInsert = '''
            insert into info(id,title,pubdates,durations,genres,countries,image,summary)
            values('{id}','{title}','{pubdates}','{durations}','{genres}','{countries}','{image}','{summary}')
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
        if spider.name == "all_movies":
            sqltext = self.SQLInsert.format(
                id=item['ID'],
                title=pymysql.escape_string(item['title']),
                pubdates=pymysql.escape_string(item['pubdates']),
                durations=pymysql.escape_string(item['durations']),
                genres=pymysql.escape_string(item['genres']),
                countries=pymysql.escape_string(item['countries']),
                image=pymysql.escape_string(item['image']),
                summary=pymysql.escape_string(item['summary']))
            self.cursor.execute(sqltext)
        return item

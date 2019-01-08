# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi

class ZhihuspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlTwistedPipline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    # scrapy 提供将 settings.py 值传进来
    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host = settings['MYSQL_HOST'],
            db = settings['MYSQL_DBNAME'],
            user = settings['MYSQL_USER'],
            passwd = settings['MYSQL_PASSWORD'],
            charset = 'utf8',
            use_unicode=True,
            cursorclass = MySQLdb.cursors.DictCursor,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)
        return item

    def handle_error(self, failure, item, spider):
        # 处理异步插入操作的异常
        # 你不知道 那个 item 出问题 所以 可以将 item 传进来
        print(failure)

    def do_insert(self, cursor, item):
        # 具体插入逻辑  根据不同的 item 做不同的 插入逻辑
        # if item.__class__.__name__ == 'JobBoleArticleItem':
        #     insert_sql = '''
        #                 insert into article (title, url, create_date, fav_nums, url_object_id, tags, praise_nums, comment_nums, front_image_url, front_image_path) values (%s, %s, %s ,%s, %s, %s, %s, %s, %s, %s)
        #             '''
        #     list = [item["title"], item["url"], item["create_date"], item["fav_nums"], item["url_object_id"], item["tags"], item["praise_nums"], item["comment_nums"], item["front_image_url"][0], item["front_image_path"]]
        #     cursor.execute(insert_sql, list)
        #     此处无需 conn.commit scrapy 自动帮你提交了

        # 或者直接将 插入逻辑 写在 对应  item 类中
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)



